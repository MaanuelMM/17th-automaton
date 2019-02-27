#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón, Eduardo Marqués De La Fuente, José Carlos Gago Hernández
# Created:      2019/02/27
# Last update:  2019/02/27
"""Exception classes shared by all finite automata."""


class FiniteAutomatonException(Exception):
    """The base class for all finite automaton-related errors."""

    pass


class InvalidStateError(FiniteAutomatonException):
    """A state is not a valid state for this finite automaton."""

    pass


class InvalidSymbolError(FiniteAutomatonException):
    """A symbol is not a valid symbol for this finite automaton."""

    pass


class MissingStateError(FiniteAutomatonException):
    """A state is missing from the finite automaton definition."""

    pass


class MissingSymbolError(FiniteAutomatonException):
    """A symbol is missing from the finite automaton definition."""

    pass


class InitialStateError(FiniteAutomatonException):
    """The initial state fails to meet some required condition."""

    pass


class FinalStateError(FiniteAutomatonException):
    """A final state fails to meet some required condition."""

    pass


class RejectionException(FiniteAutomatonException):
    """The input was rejected by the finite automaton."""

    pass
