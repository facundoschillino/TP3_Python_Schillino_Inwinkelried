"""Librería con clases para los TPs de SO I en UCSE DAR

>>> p = Proceso(0, 'P0', 2, 5)
>>> print(p)
0 - -->
>>> p
<Proceso: 0 - -->>
>>> p.listo()
>>> p.esperar()
>>> p.ejecutar()
>>> p.estadisticas()
OrderedDict([('ejecutado', 1), ('espera', 1), ('servicio', 2), ('indice', 2.5), ('historia', ['-->', ' ', '░░'])])
"""

from collections import OrderedDict

EJE = u'\u2588\u2588'
ESP = u'\u2591\u2591'
FIN = u'F'


class Proceso(object):
    """Representación de un proceso del sistema operativo

    >>> p = Proceso(1, 'P1', 0, 10)
    >>> print(p)
    1 - -->
    >>> p
    <Proceso: 1 - -->>
    >>> p.listo()
    >>> p.ejecutar()
    >>> p.esperar()
    >>> p.ejecutar()
    >>> for k, v in p.estadisticas().items():
    ...     print("{}: {}".format(k, v))
    ejecutado: 2
    espera: 1
    servicio: 3
    indice: 3.3333333333333335
    historia: ['-->', ' ', '██', '░░']
    """

    def __init__(self, id=None, nombre=None, inicio=None, duracion=None):
        """Inicialización del objeto"""
        self.id = id
        self.nombre = nombre
        self.inicio = inicio
        self.duracion = duracion
        self.procesado = 0
        self.espera = 0
        self.quantum = 0
        self.estado = '-->'
        self.historia = []

    def __str__(self):
        """Representación unicode del objeto"""
        return f"{self.id} - {self.estado}"

    def __repr__(self):
        """Representación genérica del objeto"""
        return f"<Proceso: {self}>"

    def __cambiar_estado(self, nuevo_estado):
        """Asigna el nuevo estado y guarda el anterior en la historia"""
        self.historia.append(self.estado)
        self.estado = nuevo_estado

    def ejecutar(self):
        """Cambia el estado a ejecución e incrementa el contador"""
        self.__cambiar_estado(EJE)
        self.procesado += 1

    def esperar(self):
        """Cambia el estado a espera e incrementa el contador"""
        self.__cambiar_estado(ESP)
        self.espera += 1

    def listo(self):
        """Cambia el estado a listo"""
        self.__cambiar_estado(' ')

    def estadisticas(self):
        """Retorna las estadísticas del proceso"""
        _ts = self.procesado + self.espera
        return OrderedDict({
            'ejecutado': self.procesado,
            'espera': self.espera,
            'servicio': _ts,
            'indice': self.duracion / float(_ts if _ts > 0 else 1),
            'historia': self.historia
        })

    def fin(self):
        """Retorna verdadero si el proceso ha finalizado su ejecución"""
        if self.procesado >= self.duracion and self.estado != FIN:
            self.terminar()
        return self.procesado >= self.duracion

    def terminar(self):
        """Cambia el estado a Finalizado"""
        self.__cambiar_estado(FIN)


if __name__ == '__main__':
    # Si ejecuto el módulo realizo los tests
    import doctest
    doctest.testmod(report=True, verbose=True, exclude_empty=True)
