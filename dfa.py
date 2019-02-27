#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón, Eduardo Marqués De La Fuente, José Carlos Gago Hernández
# Created:      2019/02/27
# Last update:  2019/02/27
"""Classes and methods for working with deterministic finite automata."""

import copy
import itertools
import queue

import fa
import exceptions


class DFA(fa.FA):
    """A deterministic finite automaton."""

    def __init__(self, *, states, input_symbols, transitions,
                 initial_state, final_states):
        """Initialize a complete DFA."""
        self.states = states.copy()
        self.input_symbols = input_symbols.copy()
        self.transitions = copy.deepcopy(transitions)
        self.initial_state = initial_state
        self.final_states = final_states.copy()
        self.validate()

    def _validate_transition_missing_symbols(self, start_state, paths):
        """Raise an error if the transition input_symbols are missing."""
        for input_symbol in self.input_symbols:
            if input_symbol not in paths:
                raise exceptions.MissingSymbolError(
                    'state {} is missing transitions for symbol {}'.format(
                        start_state, input_symbol))

    def _validate_transition_invalid_symbols(self, start_state, paths):
        """Raise an error if transition input symbols are invalid."""
        for input_symbol in paths.keys():
            if input_symbol not in self.input_symbols:
                raise exceptions.InvalidSymbolError(
                    'state {} has invalid transition symbol {}'.format(
                        start_state, input_symbol))

    def _validate_transition_start_states(self):
        """Raise an error if transition start states are missing."""
        for state in self.states:
            if state not in self.transitions:
                raise exceptions.MissingStateError(
                    'transition start state {} is missing'.format(
                        state))

    def _validate_transition_end_states(self, start_state, paths):
        """Raise an error if transition end states are invalid."""
        for end_state in paths.values():
            if end_state not in self.states:
                raise exceptions.InvalidStateError(
                    'end state {} for transition on {} is not valid'.format(
                        end_state, start_state))

    def _validate_transitions(self, start_state, paths):
        """Raise an error if transitions are missing or invalid."""
        self._validate_transition_missing_symbols(start_state, paths)
        self._validate_transition_invalid_symbols(start_state, paths)
        self._validate_transition_end_states(start_state, paths)

    def _validate_initial_state(self):
        """Raise an error if the initial state is invalid."""
        if self.initial_state not in self.states:
            raise exceptions.InvalidStateError(
                '{} is not a valid initial state'.format(self.initial_state))

    def _validate_final_states(self):
        """Raise an error if any final states are invalid."""
        invalid_states = self.final_states - self.states
        if invalid_states:
            raise exceptions.InvalidStateError(
                'final states are not valid ({})'.format(
                    ', '.join(invalid_states)))

    def validate(self):
        """Return True if this DFA is internally consistent."""
        self._validate_transition_start_states()
        for start_state, paths in self.transitions.items():
            self._validate_transitions(start_state, paths)
        self._validate_initial_state()
        self._validate_final_states()
        return True

    @staticmethod
    def _stringify_states(states):
        """Stringify the given set of states as a single state name."""
        return '{{{}}}'.format(','.join(sorted(states)))

    @classmethod
    def _add_nfa_states_from_queue(cls, nfa, current_states,
                                   current_state_name, dfa_states,
                                   dfa_transitions, dfa_final_states):
        """Add NFA states to DFA as it is constructed from NFA."""
        dfa_states.add(current_state_name)
        dfa_transitions[current_state_name] = {}
        if (current_states & nfa.final_states):
            dfa_final_states.add(current_state_name)

    @classmethod
    def _enqueue_next_nfa_current_states(cls, nfa, current_states,
                                         current_state_name, state_queue,
                                         dfa_transitions):
        """Enqueue the next set of current states for the generated DFA."""
        for input_symbol in nfa.input_symbols:
            next_current_states = nfa._get_next_current_states(
                current_states, input_symbol)
            dfa_transitions[current_state_name][input_symbol] = (
                cls._stringify_states(next_current_states))
            state_queue.put(next_current_states)

    @classmethod
    def from_nfa(cls, nfa):
        """Initialize this DFA as one equivalent to the given NFA."""
        dfa_states = set()
        dfa_symbols = nfa.input_symbols
        dfa_transitions = {}
        # equivalent DFA states states
        nfa_initial_states = nfa._get_lambda_closure(nfa.initial_state)
        dfa_initial_state = cls._stringify_states(nfa_initial_states)
        dfa_final_states = set()

        state_queue = queue.Queue()
        state_queue.put(nfa_initial_states)
        while not state_queue.empty():

            current_states = state_queue.get()
            current_state_name = cls._stringify_states(current_states)
            if current_state_name in dfa_states:
                # We've been here before and nothing should have changed.
                continue
            cls._add_nfa_states_from_queue(nfa, current_states,
                                           current_state_name, dfa_states,
                                           dfa_transitions, dfa_final_states)
            cls._enqueue_next_nfa_current_states(
                nfa, current_states, current_state_name, state_queue,
                dfa_transitions)

        return cls(
            states=dfa_states, input_symbols=dfa_symbols,
            transitions=dfa_transitions, initial_state=dfa_initial_state,
            final_states=dfa_final_states)
