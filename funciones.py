"""Librería con funciones para los TPs de SO I en UCSE DAR"""

import json
import os
import sys
from io import StringIO
from clases import Proceso


def dict2object(clase, datos):
    """Crea un objeto desde un diccionario

    Recibe una "Clase" para instanciar y un diccionario con los datos a cargar
    en el objeto.

    >>> class P():
    ...     pass
    >>> d = {'Atributo1': 'Valor1', 'Atributo2': 'Valor2'}
    >>> o = dict2object(P, d)
    >>> o.Atributo1
    'Valor1'
    >>> o.Atributo2
    'Valor2'
    """

    objeto = clase()
    for key, value in datos.items():
        setattr(objeto, key, value)

    return objeto


def load_from_json(filename):
    """Carga los datos desde un archivo JSON"""
    if os.path.isfile(filename):
        procesos = []
        datos = json.load(open(filename, 'r'))
        for value in datos.values():
            procesos.append(dict2object(Proceso, value))
        return procesos
    else:
        raise Exception("El archivo solicitado no existe")


class Capturing(list):
    """Class to capture stdout"""

    def __init__(self):
        self._stdout = None
        self._stringio = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


if __name__ == '__main__':
    # Si ejecuto el módulo realizo los tests
    import doctest
    doctest.testmod(report=True, verbose=True)
