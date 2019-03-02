#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/28
# Last update:  2019/03/02
"""Clases y métodos para trabajar con autómatas finitos."""

import copy
import queue


class AF:
    """Un autómata finito."""

    # Completo
    def __init__(self, *, estados, alfabeto, transiciones, estado_inicial, estados_finales):
        """Inicializa un autómata finito."""
        self.estados = estados.copy()
        self.alfabeto = alfabeto.copy()
        self.transiciones = copy.deepcopy(transiciones)
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales.copy()

    # Incompleto
    def _eliminar_transiciones_vacias(self):
        """Elimina las transiciones vacías del autómata finito."""

    # Completo
    def _obtener_accesibles_de_un_estado(self, estado):
        """Devuelve los estados accesibles de un estado dado."""
        accesibles_del_estado_dado = set()
        if(estado in self.transiciones):
            for entrada in self.transiciones[estado]:
                for estado_accesible in self.transiciones[estado][entrada]:
                    accesibles_del_estado_dado.add(estado_accesible)
        return accesibles_del_estado_dado

    # Completo
    def _obtener_accesibles(self):
        """Devuelve los estados accesibles del autómata finito."""
        # Declaramos variables a utilizar
        estados_visitados = set()
        cola_estados = queue.Queue()

        # Inicializamos las variables con las del estado inicial
        estados_visitados.add(self.estado_inicial)
        for estado_accesible in self._obtener_accesibles_de_un_estado(self.estado_inicial):
            cola_estados.put(estado_accesible)

        # Realizamos bucle para obtener el resto de estados accesibles
        while(not cola_estados.empty()):
            estado_cola = cola_estados.get()
            if(estado_cola not in estados_visitados):
                estados_visitados.add(estado_cola)
                for estado_accesible in self._obtener_accesibles_de_un_estado(estado_cola):
                    cola_estados.put(estado_accesible)

        # Devolvemos la lista de estados visitados, es decir, que son accesibles
        return estados_visitados

    # Incompleto
    def _obtener_coaccesibles(self):
        """Obtiene los estados co-accesibles del autómata finito."""


    # Incompleto
    def convertir_a_afd(self):
        """Convierte el autómata finito a uno determinista."""
        # ¿Hace falta eliminar las transiciones vacías previamente?
        self.estados = self._obtener_accesibles()
         # Algoritmo para ver qué estados son co-accesibles

    # Completo
    def copy(self):
        """Devuelve una copia del autómata finito."""
        return self.__class__(**vars(self))