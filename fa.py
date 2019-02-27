#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón, Eduardo Marqués De La Fuente, José Carlos Gago Hernández
# Created:      2019/02/27
# Last update:  2019/02/27
"""Classes and methods for working with all finite automata."""

import abc


class FA(metaclass=abc.ABCMeta):
    """An abstract base class for finite automata."""

    @abc.abstractclassmethod
    def __init__(self):
        """Initialize a complete finite automaton."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def validate(self):
        """Return True if this finite automaton is internally consistent."""
        raise NotImplementedError

    def copy(self):
        """Create a deep copy of the finite automaton."""
        return self.__class__(**vars(self))
