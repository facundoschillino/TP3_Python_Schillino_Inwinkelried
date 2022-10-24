# -*- coding: utf-8 *-*
"""
UCSE DAR - Sistemas Operativos I - Trabajo Práctico Nro 1

Algoritmos de Planificación del Procesador
"""
from typing import List, Optional
from clases import Proceso


__autores__ = [
    ["Santiago Inwinkelried Apellido", "email@email.com"],
    ["Facundo Schillino", "facundoschillino01@gmail.com"]
]

__all__ = [
    'FIFO', 'SJN', 'SRT', 'RoundRobin',
    'HRN', 'HRNsa',
    'Prioridad', 'PrioridadA'
]


def FIFO(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    """
    Algoritmo FIFO

    ** Requerido para regularizar **

    Algoritmo de planificación basado en la utilización de una cola FIFO.

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Los pasos deseados del algoritmo son:
        - si proceso_actual existe y no terminó, continua ejecutando proceso_actual
        - si proceso_actual no existe o terminó, se busca el siguiente a ejecutar en la lista de procesos
        - si se encuentra un siguiente, se lo ejecuta
        - si tengo un siguiente y además existen otros procesos que se podrían ejecutar, se los hace esperar
        - se retorna el siguiente (puede ser None si no se encontró un proceso a ejecutar)

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    """  Si hay un proceso ocupando el procesador:       """
    """ Si el proceso actual no terminó : pongo a los demas en espera. En este if solo se sigue ejecutando el proceso si este esta ocupando el procesador y se deja esperando a los demas"""
    if proceso_actual is not None:
        if not proceso_actual.fin():
            for proceso in cola_procesos:
                if not proceso.fin() and proceso.inicio <= tiempo_actual:
                    if proceso is not proceso_actual:
                        proceso.esperar()
            proceso_actual.ejecutar()
            return proceso_actual
        else:
            menor = cola_procesos[0]
            for proceso in cola_procesos:
                if not proceso.fin() and proceso.inicio <= tiempo_actual:
                    if menor.fin():
                        menor = proceso
                    else:
                        if proceso.inicio == menor.inicio:
                            if proceso.id < menor.id:
                                menor = proceso
                        else:
                            if proceso.inicio < menor.inicio:
                                menor = proceso
            for proceso in cola_procesos:
                if not proceso.fin() and proceso.inicio <= tiempo_actual:
                    if proceso is not menor:
                        proceso.esperar()
            if menor.inicio > tiempo_actual:
                menor = None
            else:
                if not menor.fin():
                    menor.ejecutar()
            return menor
    else:
        menor = cola_procesos[0]
        for proceso in cola_procesos:
            if not proceso.fin() and proceso.inicio <= tiempo_actual:
                if menor.fin():
                    menor = proceso
                else:
                    if proceso.inicio == menor.inicio:
                        if proceso.id < menor.id:
                            menor = proceso
                    else:
                        if proceso.inicio < menor.inicio:
                            menor = proceso
        for proceso in cola_procesos:
            if not proceso.fin() and proceso.inicio <= tiempo_actual:
                if proceso is not menor:
                    proceso.esperar()
        if menor.inicio > tiempo_actual:
            menor = None
        else:
            if not menor.fin():
                menor.ejecutar()

        return menor


def SJN(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    """
    Algoritmo SJN.

    ** Requerido para regularizar **

    Algoritmo de planificación basado en la utilización de una cola SJN.

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    if proceso_actual is not None:
        if not proceso_actual.fin():
            esperaProcesos(proceso_actual, cola_procesos, tiempo_actual)
            proceso_actual.ejecutar()
            return proceso_actual
        else:
            menor = cola_procesos[0]
            menor = SiguientePorSJN(menor, cola_procesos, tiempo_actual)
            esperaProcesos(menor, cola_procesos, tiempo_actual)
            if menor.inicio > tiempo_actual:
                menor = None
            else:
                if not menor.fin():
                    menor.ejecutar()
            return menor
    else:
        menor = cola_procesos[0]
        menor = SiguientePorSJN(menor, cola_procesos, tiempo_actual)
        esperaProcesos(menor, cola_procesos, tiempo_actual)
        if menor.inicio > tiempo_actual:
            menor = None
        else:
            if not menor.fin():
                menor.ejecutar()
        return menor


def SRT(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    """
    Algoritmo SRT (Apropiativo)

    ** Requerido para regularizar **

    Algoritmo de planificación basado en la utilización de una cola SRT.

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    menor = cola_procesos[0]
    for proceso in cola_procesos:
        if not proceso.fin() and proceso.inicio <= tiempo_actual:
            tiempo_restante_proceso = proceso.duracion - proceso.procesado
            tiempo_restante_menor = menor.duracion - menor.procesado
            if tiempo_restante_menor > tiempo_restante_proceso or menor.fin() or menor.inicio > tiempo_actual:
                menor = proceso
            else:
                if tiempo_restante_menor == tiempo_restante_proceso:
                    if proceso.id > menor.id:
                        menor = proceso
    esperaProcesos(menor, cola_procesos, tiempo_actual)
    if menor.inicio > tiempo_actual:
        menor = None
    else:
        if not menor.fin():
            menor.ejecutar()
    return menor


def HRN(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    """
    Algoritmo HRN (Apropiativo)

    Algoritmo de planificación basado en la utilización de una cola HRN.

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    # (tiempo de espera + tiempo de ejecucion)/ tiempo de ejecucion
    menor = cola_procesos[0]
    for proceso in cola_procesos:
        if not proceso.fin() and proceso.inicio <= tiempo_actual:
            PProceso = ((proceso.espera + proceso.duracion) / proceso.duracion)
            PMenor = ((menor.espera + menor.duracion) / menor.duracion)
            if PProceso > PMenor or menor.fin() or menor.inicio > tiempo_actual:
                menor = proceso
    esperaProcesos(menor, cola_procesos, tiempo_actual)
    preguntarsiestalisto(menor, tiempo_actual)





def HRNsa(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    """Algoritmo HRN (Semi-Apropiativo)

    Algoritmo de planificación basado en la utilización de una cola HRN semi-apropiativa. Las condiciones para que se
    evalúe nuevamente la prioridad de cada proceso son:
    - Que no haya proceso en ejecución
    - Que el proceso actual haya terminado
    - Que algún otro proceso inicie en este instante

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    if proceso_actual is not None:
        if not proceso_actual.fin():
            esperaProcesos(proceso_actual, cola_procesos, tiempo_actual)
            proceso_actual.ejecutar()
            return proceso_actual
        else:
            menor = cola_procesos[0]
            for proceso in cola_procesos:
                if not proceso.fin() and proceso.inicio <= tiempo_actual:
                    PProceso = ((proceso.espera + proceso.duracion) / proceso.duracion)
                    PMenor = ((menor.espera + menor.duracion) / menor.duracion)
                    if PProceso > PMenor or menor.fin() or menor.inicio > tiempo_actual:
                        menor = proceso
            esperaProcesos(menor, cola_procesos, tiempo_actual)
            if menor.inicio > tiempo_actual:
                menor = None
            else:
                if not menor.fin():
                    menor.ejecutar()
            return menor
    else:
        menor = cola_procesos[0]
        for proceso in cola_procesos:
            if not proceso.fin() and proceso.inicio >= tiempo_actual:
                PProceso = ((proceso.espera + proceso.duracion) / proceso.duracion)
                PMenor = ((menor.espera + menor.duracion) / menor.duracion)
                if PProceso > PMenor or menor.fin() or menor.inicio < tiempo_actual:
                    menor = proceso
        esperaProcesos(menor, cola_procesos, tiempo_actual)
        if menor.inicio > tiempo_actual:
            menor = None
        else:
            if not menor.fin():
                menor.ejecutar()
        return menor



def Prioridad(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    if proceso_actual is not None:
        if not proceso_actual.fin():
            esperaProcesos(proceso_actual, cola_procesos, tiempo_actual)
            proceso_actual.ejecutar()
            return proceso_actual
        else:
            menor = cola_procesos[0]
            menor = SiguientePorPrioridad(menor, cola_procesos, tiempo_actual)
            esperaProcesos(menor, cola_procesos, tiempo_actual)
            preguntarsiestalisto(menor, tiempo_actual)
    else:
        menor = cola_procesos[0]
        menor = SiguientePorPrioridad(menor, cola_procesos, tiempo_actual)
        esperaProcesos(menor, cola_procesos, tiempo_actual)
        if menor.inicio > tiempo_actual:
            menor = None
        else:
            if not menor.fin():
                menor.ejecutar()
        return menor


def PrioridadA(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int):
    """
    Algoritmo por Prioridad (Apropiativo)

    Algoritmo de planificación basado en la utilización de una cola por Prioridad.

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    # TODO: codificar
    menor = cola_procesos[0]
    for proceso in cola_procesos:
        if not proceso.fin() and proceso.inicio <= tiempo_actual:
            if menor.prioridad < proceso.prioridad or menor.fin() or menor.inicio > tiempo_actual:
                menor = proceso
            else:
                if menor.prioridad == proceso.prioridad:
                    if proceso.id > menor.id:
                        menor = proceso
    esperaProcesos(menor, cola_procesos, tiempo_actual)
    preguntarsiestalisto(menor, tiempo_actual)


def RoundRobin(proceso_actual: Optional[Proceso], cola_procesos: Optional[List[Proceso]], tiempo_actual: int,
               quantum: int):
    """
    Algoritmo RoundRobin (Apropiativo)

    ** Requerido para regularizar **

    Algoritmo de planificación basado en la utilización de una cola por RoundRobin.

    En base al proceso actual, la cola de procesos y el tiempo actual, la función debe retornar el siguiente proceso a
    ejecutar.

    Args:
        proceso_actual: Proceso: proceso que está actualmente haciendo uso del procesador
        cola_procesos: list: lista con los todos los procesos
        tiempo_actual: int: instante de ejecución actual
        quantum: int: quantum máximo del que dispone un proceso para uso del procesador

    Returns:
        Proceso: siguiente proceso a ejecutar
        None: si no se encuentra un proceso a ejecutar
    """
    # TODO: codificar
    if proceso_actual is not None :
        if not proceso_actual.fin() and proceso_actual.quantum < quantum and proceso_actual.inicio >= tiempo_actual:
            esperaProcesos(proceso_actual, cola_procesos, tiempo_actual)
            proceso_actual.ejecutar()
            proceso_actual.quantum += 1
            return proceso_actual
        else:
            menor = cola_procesos[0]
            for proceso in cola_procesos:
                if not proceso.fin() and proceso.inicio <= tiempo_actual and proceso.quantum < quantum and proceso != proceso_actual:
                    if menor.fin() or menor.quantum >= quantum:
                        menor.quantum = 0
                        menor = proceso
                    else:
                        if proceso.inicio == menor.inicio:
                            if proceso.id < menor.id:
                                menor = proceso
                        else:
                            if proceso.inicio < menor.inicio:
                                menor = proceso
            esperaProcesos(menor, cola_procesos, tiempo_actual)
            if menor.inicio > tiempo_actual:
                menor = None
            else:
                if not menor.fin():
                    menor.ejecutar()
                    menor.quantum += 1
            return menor
    else:
        menor = cola_procesos[0]
        for proceso in cola_procesos:
            if not proceso.fin() and proceso.inicio <= tiempo_actual and proceso.quantum < quantum:
                if menor.fin() or menor.quantum >= quantum:
                    menor.quantum = 0
                    menor = proceso
                else:
                    if proceso.inicio == menor.inicio:
                        if proceso.id < menor.id:
                            menor = proceso
                    else:
                        if proceso.inicio < menor.inicio:
                            menor = proceso
        esperaProcesos(menor, cola_procesos, tiempo_actual)

        if menor.inicio > tiempo_actual:
            menor = None
        else:
            if not menor.fin():
                menor.ejecutar()
                menor.quantum += 1
        return menor





def preguntarsiestalisto (menor : Proceso, tiempo_actual : int):
    if menor.inicio > tiempo_actual:
        menor = None
    else:
        if not menor.fin():
            menor.ejecutar()
    return menor


def esperaProcesos(procesoingresado: Proceso, cola_procesos: List[Proceso], tiempo_actual: int):
    for proceso in cola_procesos:
        if not proceso.fin() and proceso.inicio <= tiempo_actual:
            if proceso is not procesoingresado:
                proceso.esperar()


def SiguientePorPrioridad(procesoingresado: Proceso, cola_procesos: List[Proceso], tiempo_actual: int):
    for proceso in cola_procesos:
        if not proceso.fin() and proceso.inicio <= tiempo_actual:
            if procesoingresado.prioridad < proceso.prioridad or procesoingresado.fin() or procesoingresado.inicio > tiempo_actual:
                procesoingresado = proceso
            else:
                if procesoingresado.prioridad == proceso.prioridad:
                    if proceso.id > procesoingresado.id:
                        procesoingresado = proceso
    return procesoingresado


def SiguientePorSJN(procesoingresado: Proceso, cola_procesos: List[Proceso], tiempo_actual: int):
    for proceso in cola_procesos:
        if not proceso.fin() and proceso.inicio <= tiempo_actual:
            if procesoingresado.duracion > proceso.duracion or procesoingresado.fin() or procesoingresado.inicio > tiempo_actual:
                procesoingresado = proceso
    return procesoingresado

def SiguientePorSRT(proceso_ingresado: Proceso, cola_procesos: list[Proceso], tiempo_restante_proceso_actual: int, tiempo_actual : int):

    for proceso in cola_procesos:
        tiempo_restante_proceso = proceso.duracion - proceso.procesado
        if tiempo_restante_proceso < tiempo_restante_proceso_actual and proceso.inicio > tiempo_actual:
            if proceso_ingresado is not None:
                    proceso_ingresado = proceso
    return proceso_ingresado
