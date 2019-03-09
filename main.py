#!/usr/bin/env python3
# Authors:      Manuel Martín Malagón
#               Eduardo Marqués De La Fuente
#               José Carlos Gago Hernández
# Created:      2019/02/27
# Last update:  2019/03/09

from af import AF


opciones_menu = {
    1: "Introducir y convertir un autómata finito",
    0: "Salir"
}

opciones_leer = {
    1: "Seguir leyendo",
    0: "Finalizar lectura"
}

def imprimir_opciones(opciones):
    for x in opciones:
        print(x,":",opciones[x])

def banner():
    print("Copyright © 2019 Manuel Martín Malagón, Eduardo Marqués De La Fuente and José Carlos Gago Hernández")
    print("Released under the MIT license")
    print()
    print(" _____________   __  .__                             __                         __                 ")
    print("/_   \\______  \\_/  |_|  |__           _____   __ ___/  |_  ____   _____ _____ _/  |_  ____   ____  ")
    print(" |   |   /    /\\   __\\  |  \\   ______ \\__  \\ |  |  \\   __\\/  _ \\ /     \\\\__  \\\\   __\\/  _ \\ /    \\ ")
    print(" |   |  /    /  |  | |   Y  \\ /_____/  / __ \\|  |  /|  | (  <_> )  Y Y  \\/ __ \\|  | (  <_> )   |  \\")
    print(" |___| /____/   |__| |___|  /         (____  /____/ |__|  \\____/|__|_|  (____  /__|  \\____/|___|  /")
    print("                          \\/               \\/                         \\/     \\/                 \\/ ")
    print()

def leer(algo, estados=False, más=True):
    conjunto = set()
    while True:
        # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
        lectura = ''.join(input("Introduzca el nombre de " + algo +":\n").split())
        if(lectura != ''):
            if(estados):
                if(lectura not in estados):
                    print("El estado " + lectura + "no está dentro de los estados posibles.")
                    print("¡RECUERDA! Los estados posibles son: " + str(estados))
                else:
                    break
            else:
                break
        else:
            print("El nombre de " + algo + " es vacío. Por favor, introduzca un nombre válido.\n")
    conjunto.add(lectura)
    if(más):
        while True:
            imprimir_opciones(opciones_leer)
            eleccion = ''.join(input("Seleccione una opción:\n").split())
            if(eleccion == str(0)):
                break
            elif(eleccion == str(1)):
                conjunto.update(leer(algo, estados, más))
                break
            else:
                print("Opción incorrecta. Por favor, introduzca una opción correcta entre las indicadas.\n")
    return conjunto

def leer_estados():
    print("-----------------------------------------LECTURA DE ESTADOS-----------------------------------------")
    return leer("estado")

def leer_alfabeto():
    print("----------------------------------------LECTURA DEL ALFABETO----------------------------------------")
    return leer("entrada")

def leer_transiciones(estados, alfabeto):
    print("--------------------------------------LECTURA DE TRANSICIONES---------------------------------------")
    transiciones = {}
    alfabeto_con_lambda = alfabeto.copy()
    alfabeto_con_lambda.add('')
    for estado in estados:
        print("Estado: -" + estado + "-")
        transiciones[estado] = {}
        for entrada in alfabeto_con_lambda:
            while True:
                print("¿Desea añadir transiciones con la entrada -" + entrada + "-?")
                imprimir_opciones(opciones_leer)
                eleccion = ''.join(input("Seleccione una opción:\n").split())
                if(eleccion == str(0)):
                    break
                elif(eleccion == str(1)):
                    transiciones[estado][entrada] = leer("estado", estados)
                    break
                else:
                    print("Opción incorrecta. Por favor, introduzca una opción correcta entre las indicadas.\n")
    return transiciones

def leer_estado_inicial(estados):
    print("---------------------------------------LECTURA ESTADO INICIAL---------------------------------------")
    return leer("estado inicial", estados, False)

def leer_estados_finales(estados):
    print("--------------------------------------LECTURA ESTADOS FINALES---------------------------------------")
    return leer("estado final", estados)

def automata(estados, alfabeto, transiciones, estado_inicial, estados_finales):
    return AF(
        estados=estados,
        alfabeto=alfabeto,
        transiciones=transiciones,
        estado_inicial=estado_inicial,
        estados_finales=estados_finales
    )

def leer_y_convertir_automata():
    estados = leer_estados()
    alfabeto = leer_alfabeto()
    transiciones = leer_transiciones(estados, alfabeto)
    estado_inicial = leer_estado_inicial(estados).pop()
    estados_finales = leer_estados_finales(estados)
    automata_finito = automata(estados, alfabeto, transiciones, estado_inicial, estados_finales)
    print("-----------------------------------------------ANTES------------------------------------------------")
    automata_finito.imprimir()
    automata_finito.convertir_a_afd()
    print("----------------------------------------------DESPUÉS-----------------------------------------------")
    automata_finito.imprimir()

def menu():
    banner()
    while True:
        print("------------------------------------------------MENÚ------------------------------------------------")
        imprimir_opciones(opciones_menu)
        eleccion = ''.join(input("Seleccione una opción:\n").split())
        if(eleccion == str(0)):
            print("Saliendo del programa...")
            break
        elif(eleccion == str(1)):
            print("Escogida la opción número 1")
            leer_y_convertir_automata()
        else:
            print("Opción incorrecta. Por favor, introduzca una opción correcta entre las indicadas.\n")

if __name__ == "__main__":
    menu()