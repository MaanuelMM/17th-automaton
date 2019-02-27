#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón, Eduardo Marqués De La Fuente, José Carlos Gago Hernández
# Created:      2019/02/27
# Last update:  2019/02/27

from nfa import NFA
from dfa import DFA

def first_NFA():
    return NFA(
        states={'q0', 'q1', 'q2', 'q3', 'q4'},
        input_symbols={'a', 'b', 'c'},
        transitions={
            'q0': {'a': {'q2'}, 'b': {'q1', 'q2'}},
            'q1': {'a': {'q1'}, 'b': {'q1'}, 'c': {'q1', 'q2'}},
            'q2': {'a': {'q3'}, 'b': {'q2', 'q3'}},
            'q3': {'a': {'q4'}, 'b': {'q2'}},
            'q4': {'c': {'q2'}}
        },
        initial_state='q0',
        final_states={'q4'}
    )

def second_NFA():
    return NFA(
        states={'S', 'A', 'B', 'C', 'D', 'E', 'F'},
        input_symbols={'a', 'b', 'c'},
        transitions={
            'S': {'a': {'A', 'D', 'F'}, 'b': {'C', 'D', 'F'}},
            'A': {},
            'B': {'b': {'A', 'B', 'F'}},
            'C': {},
            'D': {'a': {'C'}, 'c': {'E'}},
            'E': {'b': {'F'}},
            'F': {}
        },
        initial_state='S',
        final_states={'F'}
    )


if __name__ == "__main__":
    first_DFA = DFA.from_nfa(first_NFA())
    print(first_DFA.states)
    print()
    print(first_DFA.input_symbols)
    print()
    print(first_DFA.transitions)
    print()
    print(first_DFA.initial_state)
    print()
    print(first_DFA.final_states)
    second_DFA = DFA.from_nfa(second_NFA())
    print(second_DFA.states)
    print()
    print(second_DFA.input_symbols)
    print()
    print(second_DFA.transitions)
    print()
    print(second_DFA.initial_state)
    print()
    print(second_DFA.final_states)