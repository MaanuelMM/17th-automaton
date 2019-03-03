#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/28
# Last update:  2019/03/03
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

        # Comprobamos si existen transiciones del estado indicando
        if(estado in self.transiciones):
            for entrada in self.transiciones[estado]:
                for estado_accesible in self.transiciones[estado][entrada]:
                    accesibles_del_estado_dado.add(estado_accesible)
        
        # Devolvemos los estados accesibles
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

    # Completo
    def _eliminar_estados_no_accesibles_de_transiciones(self):
        """Eliminar los estados no accesibles de las transiciones posibles."""
        transiciones_nuevo = copy.deepcopy(self.transiciones)

        for estado in self.transiciones:
            # Si existe un estado en las transiciones que no está en los estados del AF,
            # eliminamos todas las transiciones posibles desde este
            if(estado not in self.estados):
                transiciones_nuevo.pop(estado)
            # No contemplamos el caso en el que un estado existente pueda transitar a uno
            # no existente, pues únicamente estamos eliminando aquellos estados que no son
            # accesibles, y no los que no son co-accesibles

        self.transiciones = transiciones_nuevo

    # Completo
    def _eliminar_estados_no_coaccesibles_de_transiciones(self):
        """Eliminar los estados no co-accesibles de las transiciones posibles."""
        transiciones_nuevo = copy.deepcopy(self.transiciones)

        for estado in self.transiciones:
            # Si existe un estado en las transiciones que no está en los estados del AF,
            # eliminamos todas las transiciones posibles desde este
            if(estado not in self.estados):
                transiciones_nuevo.pop(estado)
            # En el caso de que el estado visitado esté dentro de los estados posibles
            # del AF, veremos si este transita a un estado que no exista en el AF
            # (esta última parte se puede omitir si únicamente hemos eliminado los
            # estados que no son accesibles, pero no los co-accesibles)
            else:
                for entrada in self.transiciones[estado]:
                    for estado_accesible in self.transiciones[estado][entrada]:
                        if(estado_accesible not in self.estados):
                            transiciones_nuevo[estado][entrada].remove(estado_accesible)
                    if(not transiciones_nuevo[estado][entrada]):
                        transiciones_nuevo[estado].pop(entrada)
                if(not transiciones_nuevo[estado]):
                    transiciones_nuevo.pop(estado)

        self.transiciones = transiciones_nuevo


    # Completo
    def _eliminar_estados_finales_no_existentes(self):
        """Elimina los estados finales que no existen."""
        estados_finales_nuevo = self.estados_finales.copy()

        for estado in self.estados_finales:
            if(estado not in self.estados):
                estados_finales_nuevo.remove(estado)
        
        self.estados_finales = estados_finales_nuevo

    # Completo
    def _eliminar_estados_no_accesibles(self):
        """Elimina los estados no accesibles del autómata finito."""
        self._eliminar_estados_no_accesibles_de_transiciones()
        self._eliminar_estados_finales_no_existentes()

    # Completo
    def _eliminar_estados_no_coaccesibles(self):
        """Elimina los estados no co-accesibles del autómata finito."""
        self._eliminar_estados_no_coaccesibles_de_transiciones()
        self._eliminar_estados_finales_no_existentes()

    # Completo
    def _obtener_coaccesibles_de_un_estado(self, estado):
        """Devuelve los estados co-accesibles de un estado dado."""
        coaccesibles_del_estado_dado = set()

        # https://stackoverflow.com/questions/6346492/how-to-stop-a-for-loop
        # https://www.digitalocean.com/community/tutorials/how-to-use-break-continue-and-pass-statements-when-working-with-loops-in-python-3
        for estado_transitable in self.transiciones:
            for entrada in self.transiciones[estado_transitable]:
                for estado_accesible in self.transiciones[estado_transitable][entrada]:
                    if(estado_accesible == estado):
                        coaccesibles_del_estado_dado.add(estado_transitable)
                        break
                else:
                    continue
                break
        
        return coaccesibles_del_estado_dado

    # Completo
    def _obtener_coaccesibles(self):
        """Obtiene los estados co-accesibles del autómata finito."""
        # Declaramos e inicializamos variables a utilizar
        estados_visitados = self.estados_finales.copy()
        cola_estados = queue.Queue()
        for estado_final in self.estados_finales:
            for estado_coaccesible in self._obtener_coaccesibles_de_un_estado(estado_final):
                cola_estados.put(estado_coaccesible)

        # Realizamos bucle para obtener el resto de estados co-accesibles
        while(not cola_estados.empty()):
            estado_cola = cola_estados.get()
            if(estado_cola not in estados_visitados):
                estados_visitados.add(estado_cola)
                for estado_coaccesible in self._obtener_coaccesibles_de_un_estado(estado_cola):
                    cola_estados.put(estado_coaccesible)

        # Devolvemos la lista de estados visitados, es decir, que son co-accesibles
        return estados_visitados

    # Incompleto
    def convertir_a_afd(self):
        """Convierte el autómata finito a uno determinista."""
        # ¿Hace falta eliminar las transiciones vacías previamente?
        self.estados = self._obtener_accesibles()
        self._eliminar_estados_no_accesibles()
        self.estados = self._obtener_coaccesibles()
        self._eliminar_estados_no_coaccesibles()

    # Completo
    def copy(self):
        """Devuelve una copia del autómata finito."""
        return self.__class__(**vars(self))