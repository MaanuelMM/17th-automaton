#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/03/11
# Last update:  2019/03/11

from af import AF


def primer_AF():
    return AF(
        estados={'q0', 'q1', 'q2', 'q3', 'q4'},
        alfabeto={'a', 'b', 'c'},
        transiciones={
            'q0': {
                'a': {'q2'},
                'b': {'q1', 'q2'}
            },
            'q1': {
                'a': {'q1'},
                'b': {'q1'},
                'c': {'q1', 'q2'}
            },
            'q2': {
                'a': {'q3'},
                'b': {'q2', 'q3'},
            },
            'q3': {
                'a': {'q4'},
                'b': {'q2'},
            },
            'q4': {
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
            },
            'A': {},
            'B': {
                'b': {'A', 'B', 'F'},
            },
            'C': {},
            'D': {
                'a': {'C'},
                'c': {'E'}
            },
            'E': {
                'b': {'F'},
            },
            'F': {}
        },
        estado_inicial='S',
        estados_finales={'F'}
    )


if __name__ == "__main__":
    # Creamos los autómatas finitos
    primer_AF = primer_AF()
    segundo_AF = segundo_AF()

    # Realizamos lo que pide el enunciado
    primer_AF.convertir_17th_automaton()
    segundo_AF.convertir_17th_automaton()
    
    # Autómatas resultantes de lo que pide el enunciado
    print("Primer AF:")
    primer_AF.imprimir()

    print("Segundo AF:")
    segundo_AF.imprimir()