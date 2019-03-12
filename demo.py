#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/03/11
# Last update:  2019/03/12

from af import AF
from main import banner

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

def convertir_y_mostrar_automata(automata):
    # Mostramos la creación del autómata finito
    print("\nANTES:")
    automata.imprimir()
    # Realizamos lo que pide el enunciado y mostramos lo que sucede con el autómata
    automata.convertir_a_17th_automaton()
    print("\n\nDESPUÉS:")
    automata.imprimir()    


if __name__ == "__main__":
    banner()
    # Creamos los dos autómatas finitos de ejemplo
    primer_AF = primer_AF()
    segundo_AF = segundo_AF()

    # Mostramos la creación del primer autómata finito
    print("\n\n\n---------------------------------------------PRIMER AF----------------------------------------------")
    convertir_y_mostrar_automata(primer_AF)
    print("\n----------------------------------------------------------------------------------------------------")
    
    # Mostramos la creación del segundo autómata finito
    print("\n\n---------------------------------------------SEGUNDO AF---------------------------------------------")
    convertir_y_mostrar_automata(segundo_AF)
    print("\n----------------------------------------------------------------------------------------------------")