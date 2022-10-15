#!/usr/bin/python3
"""TP 1 - Sistemas Operativos I - UCSE DAR"""

from argparse import ArgumentParser
from copy import deepcopy
from funciones import load_from_json, Capturing

DEBUG = False
SPACE = u'\u0020'


def get_command_line_params():
    """Parámetros de ejecución del script"""
    parser = ArgumentParser()
    parser.add_argument("-q", "--quantum", dest="quantum", default=2, type=int,
                        help="Valor de Quantum para usar en RR")
    parser.add_argument("-a", "--algorithm", type=str, dest="algorithm",
                        default=['FIFO', 'SJN', 'SRT', 'RoundRobin', 'HRN', 'HRNsa', 'Prioridad', 'PrioridadA'],
                        nargs='*', help="Algoritmos a ejecutar (None = Todos)")
    parser.add_argument("-d", "--datafile", type=str, dest="datafile", default='data.json',
                        help="Set de datos a utilizar")
    parser.add_argument("-m", "--module", type=str, dest="module", default=['alumno'], nargs='*',
                        help="Módulo de donde cargar las funciones")
    parser.add_argument("-t", "--time", type=int, dest="time", default=50, help="Tiempo máximo a utilizar")
    parser.add_argument("--verbose", action="store_true", help="Mostrar mas detalle de las excepciones")
    return parser.parse_args()


def ejecutar(algoritmos, procesos, quantum, tiempo):
    """Realiza la ejecución de los algoritmos"""
    ejecuciones = {a.__name__: None for a in algoritmos}
    exceptions = 0

    for algoritmo in algoritmos:
        _procs = [deepcopy(c) for c in procesos]  # Copio los procesos
        ciclos = -1  # Inicializo en -1 para que el 1er tiempo sea 0
        actual = None
        try:
            while any([not c.fin() for c in _procs]) and ciclos < tiempo:
                ciclos += 1
                try:
                    params = [actual, _procs, ciclos]
                    if algoritmo.__name__ == 'RoundRobin':
                        params += [quantum]
                    actual = algoritmo(*params)
                except NotImplementedError as exception:
                    raise exception
                # Actualizo la historia para los que no procesan ni esperan
                for proc in _procs:
                    if len(proc.historia) == ciclos and not proc.fin():
                        proc.listo()
            _procs.sort(key=lambda x: x.id)
            ejecuciones[algoritmo.__name__] = _procs
        except NotImplementedError:
            ejecuciones[algoritmo.__name__] = []

    if exceptions > 0:
        print(f"Se detectaron errores ({exceptions}) durante la ejecución."
              " Por favor, revise el código\n")

    return ejecuciones


if __name__ == '__main__':

    options = get_command_line_params()

    if options.verbose:
        DEBUG = True

    with Capturing() as out:
        for module in options.module:
            # Importo el módulo y cargo los algoritmos disponibles
            try:
                mod = __import__(module)
            except ImportError:
                print(f"El módulo '{module}' no puede ser cargado")
                continue
            _algoritmos = {algname: getattr(mod, algname) for algname in options.algorithm if hasattr(mod, algname)}

            # Cargo los datos de los procesos a ejecutar desde el archivo data.json
            procs_data = load_from_json(options.datafile)

            # Ejecuto TODOS los algoritmos
            ejecs = ejecutar(_algoritmos.values(), procs_data, options.quantum, options.time)

            # Tiempo máximo
            if sum([len(x) for x in ejecs.values()]):
                maxtime = max([len(p.historia) for e in ejecs.values() for p in e])
            else:
                maxtime = options.time

            tblh = "%10s In Du Pr     %s   Ts  Es  I.Se"
            lenth = len(tblh % ("", "")) + (3 * maxtime)

            # Imprimo gráficas de historia de ejecución por cada algoritmo
            print("*" * lenth)
            print(", ".join("%s <%s>" % tuple(a) for a in mod.__autores__))
            print("Archivo de datos: {}".format(options.datafile))

            for al in options.algorithm:
                print("\n" + "-" * lenth)
                print(tblh % (al, " ".join(["%02d" % n for n in range(maxtime)])))
                if al in _algoritmos:
                    a = _algoritmos[al]
                    if ejecs[a.__name__] is not None and len(ejecs[a.__name__]):
                        for p in ejecs[a.__name__]:
                            _est = p.estadisticas()
                            print("%9s: %02d %02d %02d" % (p.id, p.inicio, p.duracion, p.prioridad), end=" ")
                            for e in p.historia:
                                print(e.center(2, ' '), end=" ")
                            if len(p.historia) <= maxtime:
                                print("   " * (maxtime - len(p.historia) + 1), end=" ")
                            print(" %02d  %02d  %02.2f" % (_est['servicio'], _est['espera'], _est['indice']))
                    else:
                        print("\n" + " " * 24 + "**** No implementado ****")
                else:
                    print("\n" + " " * 24 + "**** No implementado ****")

            print("\n" + "*" * lenth)

    print("\n".join(out).replace(" ", SPACE))
