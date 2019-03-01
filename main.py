#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/27
# Last update:  2019/03/01

from af import AF

def primer_AF():
    return AF(
        estados={'q0', 'q1', 'q2', 'q3', 'q4'},
        alfabeto={'a', 'b', 'c'},
        transiciones={
            'q0': {
                'a': {'q2'},
                'b': {'q1', 'q2'},
                'c': {}
            },
            'q1': {
                'a': {'q1'},
                'b': {'q1'},
                'c': {'q1', 'q2'}
            },
            'q2': {
                'a': {'q3'},
                'b': {'q2', 'q3'},
                'c': {}
            },
            'q3': {
                'a': {'q4'},
                'b': {'q2'},
                'c': {}
            },
            'q4': {
                'a': {},
                'b': {},
                'c': {'q2'}
            }
        },
        estado_inicial='q0',
        estados_finales={'q4'}
    )

def segundo_AF():
    return AF(
        estados={'S', 'A', 'B', 'C', 'D', 'E', 'F'},
        alfabeto={'a', 'b', 'c'},
        transiciones={
            'S': {
                'a': {'A', 'D', 'F'},
                'b': {'C', 'D', 'F'},
                'c': {}
            },
            'A': {
                'a': {},
                'b': {},
                'c': {}
            },
            'B': {
                'a': {},
                'b': {'A', 'B', 'F'},
                'c': {}
            },
            'C': {
                'a': {},
                'b': {},
                'c': {}
            },
            'D': {
                'a': {'C'},
                'b': {},
                'c': {'E'}
            },
            'E': {
                'a': {},
                'b': {'F'},
                'c': {}
            },
            'F': {
                'a': {},
                'b': {},
                'c': {}
            }
        },
        estado_inicial='S',
        estados_finales={'F'}
    )


if __name__ == "__main__":
    primer_AF = primer_AF()
    segundo_AF = segundo_AF()