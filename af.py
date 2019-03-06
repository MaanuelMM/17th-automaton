#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/28
# Last update:  2019/03/06
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


    # Completo
    @staticmethod
    def _hacer_string_de_conjunto_estados(estados):
        """Devuelve el conjunto de estados dado en forma de string."""
        return '{{{}}}'.format(','.join(sorted(estados)))

    # Completo
    def _obtener_próximos_estados_de_conjunto(self, conjunto_estados, entrada):
        """Devuelve el conjunto de próximos estados dado un cojunto de estados y una entrada."""
        próximos_estados = set()

        for estado in conjunto_estados:
            if(entrada in self.transiciones[estado]):
                próximos_estados.update(self.transiciones[estado].get(entrada))

        return próximos_estados

    # Completo
    def _automata_accesible_determinista(self):
        """Modifica el AF a uno determinista mediante el algoritmo de estados accesibles."""
        # Declaramos e inicializamos las variables a utilizar
        estados_nuevos = set()
        transiciones_nuevas = {}
        estado_inicial_nuevo = AF._hacer_string_de_conjunto_estados(self.estado_inicial)
        estados_finales_nuevos = set()
        estados_cola = set()
        estados_cola.add(self.estado_inicial)
        cola_estados = queue.Queue()
        cola_estados.put(estados_cola)

        # Realizamos bucle para obtener el resto de estados accesibles
        while(not cola_estados.empty()):
            estados_cola = cola_estados.get()
            estado_cola = AF._hacer_string_de_conjunto_estados(estados_cola)
            if(estado_cola not in estados_nuevos):
                # Añadimos el nuevo conjunto de estados a los nuevos estados
                estados_nuevos.add(estado_cola)
                transiciones_nuevas[estado_cola] = {}
                # Si está contenido en los estados finales del antiguo autómata,
                # se añade al nuevo conjunto de estados finales
                if(estados_cola & self.estados_finales):
                    estados_finales_nuevos.add(estado_cola)
                
                # Encolar próximos estados a iterar
                for entrada in self.alfabeto:
                    próximos_estados = self._obtener_próximos_estados_de_conjunto(
                        estados_cola, entrada)
                    transiciones_nuevas[estado_cola][entrada] = (
                        AF._hacer_string_de_conjunto_estados(próximos_estados))
                    cola_estados.put(próximos_estados)
        
        # Asignamos los nuevos atributos
        self.estados = estados_nuevos
        self.transiciones = transiciones_nuevas
        self.estado_inicial = estado_inicial_nuevo
        self.estados_finales = estados_finales_nuevos


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
    def _eliminar_estados_no_coaccesibles(self):
        """Elimina los estados no co-accesibles del autómata finito."""
        self._eliminar_estados_no_coaccesibles_de_transiciones()
        # ¿Puede un estado ser final y a la vez co-accesible?
        # Si fuera así, no debería de eliminarse, ¿verdad?
        self._eliminar_estados_finales_no_existentes()

    # Completo
    def _obtener_estados_transiciones_vacias(self, estado):
        """Devuelve los estados recorridos desde un estado con transiciones vacías."""
        # Declaramos variables a utilizar
        pila = []
        estados_recorridos = set()
        pila.append(estado)
        
        # Realizamos bucle en busca de transiciones vacías del estado dado
        while pila:
            estado_pila = pila.pop()
            if(estado_pila not in estados_recorridos):
                estados_recorridos.add(estado_pila)
                if('' in self.transiciones[estado_pila]):
                    pila.extend(self.transiciones[estado_pila][''])

        # Retornamos los estados recorridos con transiciones vacías
        return estados_recorridos

    # Completo
    def _eliminar_transiciones_vacias(self):
        """Elimina las transiciones vacías del autómata finito."""
        for estado in self.transiciones:
            estados_vacios = self._obtener_estados_transiciones_vacias(estado)
            estados_vacios.remove(estado)
            for estado_vacio in estados_vacios:
                for entrada in self.transiciones[estado_vacio]:
                    if(entrada != ''):
                        for estado_entrada in self.transiciones[estado_vacio][entrada]:
                            self.transiciones[estado][entrada].add(estado_entrada)
                if(estado_vacio in self.estados_finales):
                    self.estados_finales.add(estado_vacio)
            if('' in self.transiciones[estado]):
                self.transiciones[estado].pop('')

    # Incompleto
    def convertir_a_afd(self):
        """Convierte el autómata finito a uno determinista."""
        self._eliminar_transiciones_vacias()
        # DUDA: no sé si hay que eliminar los no co-accesibles antes o después
        self._eliminar_estados_no_coaccesibles()
        self._automata_accesible_determinista()

    # Completo
    def copy(self):
        """Devuelve una copia del autómata finito."""
        return self.__class__(**vars(self))