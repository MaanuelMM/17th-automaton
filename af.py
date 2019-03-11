#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/28
# Last update:  2019/03/11
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
        estado_inicial_set = set()
        estado_inicial_set.add(self.estado_inicial)
        estado_inicial_nuevo = AF._hacer_string_de_conjunto_estados(estado_inicial_set)
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
                    transiciones_nuevas[estado_cola][entrada] = set()
                    transiciones_nuevas[estado_cola][entrada].add(
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
        if('{}' in self.estados):
            estados_visitados.add('{}')
        set_estados = set()
        for estado_final in self.estados_finales:
            for estado_coaccesible in self._obtener_coaccesibles_de_un_estado(estado_final):
                set_estados.add(estado_coaccesible)

        # Realizamos bucle para obtener el resto de estados co-accesibles
        while(set_estados):
            estado_set = set_estados.pop()
            if(estado_set not in estados_visitados):
                estados_visitados.add(estado_set)
                for estado_coaccesible in self._obtener_coaccesibles_de_un_estado(estado_set):
                    set_estados.add(estado_coaccesible)

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
                            if('{}' in self.estados and not transiciones_nuevo[estado][entrada]):
                                transiciones_nuevo[estado][entrada].add('{}')

        self.transiciones = transiciones_nuevo

    # Completo
    def _eliminar_estados_no_coaccesibles(self):
        """Elimina los estados no co-accesibles del autómata finito."""
        self.estados = self._obtener_coaccesibles()
        self._eliminar_estados_no_coaccesibles_de_transiciones()

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

    # Completo
    def _convertir_a_afd(self):
        """Convierte el autómata finito a uno determinista."""
        self._eliminar_transiciones_vacias()
        self._automata_accesible_determinista()
        self._eliminar_estados_no_coaccesibles()

    # Completo
    @staticmethod
    def _cambiar_nombre_complementario_conjunto(conjunto, texto):
        """Cambia el nombre de un conjunto añadiendo un texto indicado."""
        conjunto_copia = conjunto.copy()
        conjunto_nuevo = set()
        while(conjunto_copia):
            elemento = conjunto_copia.pop() + texto
            conjunto_nuevo.add(elemento)
        return conjunto_nuevo

    # Completo
    def _cambiar_nombre_complementario(self, texto="'"):
        """Cambia el nombre de los estados para reflejar que es complementario."""
        transiciones_nuevas = {}
        
        for estado in self.transiciones:
            transiciones_nuevas[estado + texto] = {}
            for entrada in self.transiciones[estado]:
                transiciones_nuevas[estado + texto][entrada] = (
                    AF._cambiar_nombre_complementario_conjunto(
                    self.transiciones[estado][entrada], texto))

        self.estados = AF._cambiar_nombre_complementario_conjunto(self.estados, texto)
        self.transiciones = transiciones_nuevas
        self.estado_inicial += texto
        self.estados_finales = AF._cambiar_nombre_complementario_conjunto(self.estados_finales, texto)

    # Completo
    def _convertir_a_complementario(self):
        """Convierte un autómata finito determinista completo a uno complementario.
        
        NOTA: DEBE SER UN AUTÓMATA FINITO DETERMINISTA Y COMPLETO."""
        nuevos_estados_finales = set()

        for estado in self.estados:
            if(estado not in self.estados_finales):
                nuevos_estados_finales.add(estado)

        self.estados_finales = nuevos_estados_finales
        self._cambiar_nombre_complementario()

    # Completo
    def _multiplicar_con_su_complementario(self):
        """Multiplica un autómata finito determinista completo con su complementario."""
        complementario = self.copy()
        complementario._convertir_a_complementario()
        self.estados.update(complementario.estados)
        self.transiciones.update(complementario.transiciones)
        for estado_final in self.estados_finales:
            self.transiciones[estado_final][''] = set()
            self.transiciones[estado_final][''].add(complementario.estado_inicial)
        self.estados_finales.update(complementario.estados_finales)

    # Completo
    def convertir_a_17th_automaton(self):
        """Convertir el autómata dado a uno que cumpla con el enunciado del tema 17."""
        self._convertir_a_afd()
        self._multiplicar_con_su_complementario()
        self._eliminar_transiciones_vacias()

    # Completo
    def imprimir(self):
        """Imprime el autómata finito para poder ser visualizado."""
        print("Estados:",self.estados)
        print("Alfabeto:",self.alfabeto)
        print("Transiciones:",self.transiciones)
        print("Estado inicial:",self.estado_inicial)
        print("Estados finales:",self.estados_finales)

    # Completo
    def copy(self):
        """Devuelve una copia del autómata finito."""
        return self.__class__(**vars(self))