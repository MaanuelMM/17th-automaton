#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/28
# Last update:  2019/03/01
"""Clases y métodos para trabajar con autómatas finitos."""

import copy


class AF:
    """Un autómata finito."""

    # Completo
    def __init__(self, *, estados, alfabeto, transiciones,
                 estado_inicial, estados_finales):
        """Inicializa un autómata finito."""
        self.estados = estados.copy()
        self.alfabeto = alfabeto.copy()
        self.transiciones = copy.deepcopy(transiciones)
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales.copy()

    # Incompleto
    def _recorrer_af(self):
        """Devuelve los estados accesibles del autómata finito."""
        estados_accesibles = {}
        # Recorrer ¿en amplitud?, ¿en profundidad?, ¿da igual?
        return estados_accesibles

    # Incompleto
    def convertir_a_afd(self):
        """Convierte el autómata finito a uno determinista."""
        self.estados = self._recorrer_af()
        # Algoritmo para ver qué estados son co-accesibles

    # Completo
    def copy(self):
        """Devuelve una copia del autómata finito."""
        return self.__class__(**vars(self))