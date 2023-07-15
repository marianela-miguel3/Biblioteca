#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def mostrarMenuLindo(txt): # txt menu
  with open(txt, "r") as menu:
   for linea in menu:
     renglon=linea.split("\n")
     for linea in renglon:
       print(linea)


def limpiarPantalla(): # para limpiar la pantalla
    if sys.platform.startswith('win'):
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Unix/Linux/Mac


def salir(): #Salir del programa
   sys.exit()


def validar_input_vacio(dato): #validar que ningun input este vacio
    while True:
        valor = input(dato)
        if not valor:
            print("Ingrese el dato solicitado")
        else:
            return valor


def validar(id,longitud): #validar que los input no esten vacios, que tengan cierta cantidad de digitos y q sean numeros
    while True:
       valor=input(f'Ingrese el {id}: ')
       if not valor:
            print(f'Debes ingresar un valor para {id}')
       elif valor.isalpha():
          print("Solo puedes ingresar números")
       elif len(valor)!=longitud:
          print(f'Debes ingresar un numero de {longitud} digitos')
       elif valor.isdigit() and len(valor)==longitud:
           return valor


def consultar_disponibilidad():  # consultar disponibilidad de un libro
    isbn=validar("isbn",13)
    with open("libros.txt","r",encoding='utf-8') as libros:  # Abrir el archivo "libros.txt" en modo lectura
        for linea in libros:  # Iterar sobre cada línea del archivo
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == isbn:  # Verificar si el ISBN de la línea coincide con el ISBN ingresado
                if datos[3] == "L":  # Verificar si el estado del libro es "L" (disponible)
                    print("Disponible")  
                elif datos[3] == "P":  # Verificar si el estado del libro es "P" (prestado)
                    print("En préstamo") 
                return            
        else:
            print("Libro no encontrado") 
            return


def consultar_titulos_disponibles(): #consultar todos los titulos disponibles (L: libres)
    with open("libros.txt", "r", encoding='utf-8') as libros:  # Abrir el archivo "libros.txt" en modo lectura
        for linea in libros:  # Iterar sobre cada línea del archivo
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if len(datos) >= 4 and datos[3] == "L":  # si lista "datos" tiene una longitud de 4 o mas elementos 
                #y el estado del libro es "L" (disponible)
                print(f"{datos[0]}, {datos[1]}")  # Mostrar el ISBN y título del libro


def registrar_prestamo(): # para registrar prestamo del libro
    isbn = validar("isbn", 13)
    cliente_dni = validar("dni", 8)

    # Validar si el cliente ya tiene un libro en préstamo
    with open("clientes.txt", "r", encoding='utf-8') as clientes:
        for linea in clientes:
            datos = linea.strip().split(",")
            if datos[0] == cliente_dni and datos[4] == "O":
                print("El cliente ya tiene un libro en préstamo")
                return

    cliente_encontrado = False

    with open("clientes.txt", "r+", encoding='utf-8') as clientes:
        lineas = clientes.readlines()
        clientes.seek(0)
        for i, linea in enumerate(lineas):
            datos = linea.strip().split(",")
            if datos[0] == cliente_dni:
                datos[4] = "O"
                datos[5] = isbn
                lineas[i] = ",".join(datos) + "\n"
                cliente_encontrado = True
                break

        clientes.seek(0)
        clientes.writelines(lineas)
        clientes.truncate()

    if not cliente_encontrado:
        print("Cliente no encontrado")
        return

    libro_encontrado = False

    with open("libros.txt", "r+", encoding='utf-8') as libros:
        lineas = libros.readlines()
        libros.seek(0)
        for i, linea in enumerate(lineas):
            datos = linea.strip().split(",")
            if datos[0] == isbn:
                if datos[3] == "L":
                    datos[3] = "P"
                    datos[4] = cliente_dni
                    lineas[i] = ",".join(datos) + "\n"
                    libro_encontrado = True
                    break

        libros.seek(0)
        libros.writelines(lineas)
        libros.truncate()

    if not libro_encontrado:
        print("Libro no encontrado o no disponible")
        return

    print("Préstamo registrado")

  
def registrar_devolucion(): #para registrar la devolucion del prestamo del libro
    isbn = validar("isbn", 13)

    with open("libros.txt", "r+", encoding='utf-8') as libros:
        lineas = libros.readlines()
        libros.seek(0)
        for i, linea in enumerate(lineas):
            datos = linea.strip().split(",")
            if datos[0] == isbn:
                if datos[3] == "P":
                    datos[3] = "L"
                    datos[4] = ""
                    lineas[i] = ",".join(datos) + "\n"
                    break
        else:
            print("Libro no encontrado o no está en préstamo")
            return

        libros.seek(0)
        libros.writelines(lineas)
        libros.truncate()

    with open("clientes.txt", "r+", encoding='utf-8') as clientes:
        lineas = clientes.readlines()
        clientes.seek(0)
        for i, linea in enumerate(lineas):
            datos = linea.strip().split(",")
            if datos[5] == isbn:
                if datos[4] == "O":
                    datos[4] = "L"
                    datos[5] = ""
                    lineas[i] = ",".join(datos) + "\n"
                    break
        else:
            print("Cliente no encontrado o no está ocupado")
            return

        clientes.seek(0)
        clientes.writelines(lineas)
        clientes.truncate()

    print("Devolución registrada correctamente")


def alta_cliente():  # Agregar un cliente
    dni = validar("dni", 8)
    with open ("clientes.txt", "r") as clientes:
        for linea in clientes:  # Iterar sobre cada línea del archivo
            datos = linea.strip().split(",")
            if dni==datos[0]: #verifico que ese cliente no exista ya en la base de datos
             print("Ya existe un cliente registrado con ese dni") #muestro el mensaje
             return
        else:
         nombre = validar_input_vacio("Ingrese el nombre completo del cliente: ")  
         telefono = validar_input_vacio("Ingrese el teléfono del cliente: ")  
         direccion = validar_input_vacio("Ingrese la dirección del cliente: ") 

    nuevo_cliente = f"{dni},{nombre},{telefono},{direccion},L,"

    with open("clientes.txt", "r+", encoding='utf-8') as clientes:
        lineas = clientes.readlines()
        clientes.seek(0)
        
        # Eliminar líneas en blanco al final del archivo
        while lineas and lineas[-1].strip() == "":
            lineas.pop()

        lineas.append(nuevo_cliente + "\n")
        clientes.writelines(lineas)

    print("Cliente registrado correctamente")


def validarBajaCliente(dni):
     with open("clientes.txt", "r", encoding='utf-8') as clientes:  # Abrir el archivo "clientes.txt" en modo lectura
        for linea in clientes:  # Iterar sobre cada línea del archivo
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == dni:  # Verificar si el DNI de la línea coincide con el DNI ingresado
                estado = datos[4]  # Obtener el estado del cliente de la línea
                if estado == "L":  # Verificar si el estado es "L" (libre)
                    return True #devuelvo true
                elif estado == "O":  # Verificar si el estado es "O" (ocupado)
                    return False  # retorno falso
                      

def validarBajaLibro(isbn):
     with open("libros.txt", "r", encoding='utf-8') as libros:  
        for linea in libros:  
            datos = linea.strip().split(",") 
            if datos[0] == isbn:  
             estado = datos[3]  
             if estado == "L":  
                return True 
             elif estado == "P":  
                return False 


def consultar_estado_cliente():  # Consulta el estado del cliente
    dni = validar("dni",8)  # Solicitar al usuario el DNI del cliente

    with open("clientes.txt", "r", encoding='utf-8') as clientes:  # Abrir el archivo "clientes.txt" en modo lectura
        for linea in clientes:  # Iterar sobre cada línea del archivo
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == dni:  # Verificar si el DNI de la línea coincide con el DNI ingresado
                estado = datos[4]  # Obtener el estado del cliente de la línea
                if estado == "L":  # Verificar si el estado es "L" (libre)
                    print("Cliente libre")  
                elif estado == "O":  # Verificar si el estado es "O" (ocupado)
                    print("Cliente ocupado")  
                elif estado == "B":  # Verificar si el estado es "B" (dado de baja)
                    print("Cliente dado de baja") 
                return  
        else:
            print("Cliente no encontrado")  


def modificar_cliente():  # Modificar los datos del cliente
    dni = validar("dni",8)  

    with open("clientes.txt", "r+", encoding='utf-8') as clientes:  # Abrir el archivo "clientes.txt" en modo lectura y escritura
        lineas = clientes.readlines()  # Leer todas las líneas del archivo
        clientes.seek(0)  # Posicionar el puntero al inicio del archivo
        for i, linea in enumerate(lineas):  # Iterar sobre cada línea del archivo con su índice
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == dni:  # Verificar si el DNI de la línea coincide con el DNI ingresado
                nombre = validar_input_vacio("Ingrese el nuevo nombre del cliente: ")
                telefono = validar_input_vacio("Ingrese el nuevo teléfono del cliente: ")  
                direccion = validar_input_vacio("Ingrese la nueva dirección del cliente: ")  
                datos[1] = nombre
                datos[2] = telefono  # Actualizar datos del cliente 
                datos[3] = direccion 
                lineas[i] = ",".join(datos) + "\n"  # Unir los elementos de la lista en una cadena separada por ","
                clientes.writelines(lineas)  # Sobrescribir el archivo con las líneas actualizadas
                print("Cliente modificado correctamente")  
                return  
        else:
            print("Cliente no encontrado")  


def eliminar_cliente(): # eliminar cliente
    dni = validar("dni", 8)
    with open("clientes.txt", "r+", encoding='utf-8') as clientes:
        lineas = clientes.readlines()
        clientes.seek(0)
        for i, linea in enumerate(lineas):
            datos = linea.strip().split(",")
            if datos[0] == dni:
                estado = validarBajaCliente(datos[0])
                if estado == True:
                    lineas.pop(i)
                    clientes.truncate(0)
                    clientes.writelines(lineas)
                    print("Cliente eliminado correctamente")
                    return
                elif estado == False:
                    print("No se puede eliminar el cliente porque tiene un libro prestado")
                    return
        else:
            print("Cliente no encontrado")

    
def alta_libro():  # Añadir un libro
    isbn = validar("isbn",13)
    with open ("libros.txt","r") as libros:
        for linea in libros:
            datos=linea.strip().split(",")
            if isbn==datos[0]:
                print("El libro ya existe")
                return
        else:
         titulo = validar_input_vacio("Ingrese el título del libro: ") 
         autor = validar_input_vacio("Ingrese el autor del libro: ")  

    nuevo_cliente = f"{isbn},{titulo},{autor},L,"

    with open("libros.txt", "r+", encoding='utf-8') as libros:
        lineas = libros.readlines()
        libros.seek(0)
        
        # Eliminar líneas en blanco al final del archivo
        while lineas and lineas[-1].strip() == "":
            lineas.pop()

        lineas.append(nuevo_cliente + "\n")
        libros.writelines(lineas)

    print("Libro registrado correctamente")


def consultar_libro():  # consultar el estado de un libro
    isbn = validar("isbn",13) 

    with open("libros.txt", "r", encoding='utf-8') as libros:  # Abrir el archivo "libros.txt" en modo lectura
        for linea in libros:  # Iterar sobre cada línea del archivo
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == isbn:  # Verificar si el ISBN de la línea coincide con el ISBN ingresado
                print("Título:", datos[1])  # Mostrar el título del libro
                print("Autor:", datos[2])  # Mostrar el autor del libro
                print("Estado:", datos[3])  # Mostrar el estado del libro
                if datos[3] == "L":  # Verificar si el estado es "L" (disponible)
                    print("Libro disponible")  
                if datos[3] == "P":  # Verificar si el estado es "P" (prestado)
                    print("Libro en préstamo") 
                return  
        else:
            print("Libro no encontrado") 


def modificar_libro():  # Modificar datos de un libro
    isbn = validar("isbn",13) 

    with open("libros.txt", "r+", encoding='utf-8') as libros:  # Abrir el archivo "libros.txt" en modo lectura y escritura
        lineas = libros.readlines()  # Leer todas las líneas del archivo
        libros.seek(0)  # Posicionar el puntero al inicio del archivo
        for i, linea in enumerate(lineas):  # Iterar sobre cada línea del archivo con su índice
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == isbn:  # Verificar si el ISBN de la línea coincide con el ISBN ingresado
                titulo = validar_input_vacio("Ingrese el nuevo título del libro: ") 
                autor = validar_input_vacio("Ingrese el nuevo autor del libro: ")  
                datos[1] = titulo  # Actualizar el título del libro en la línea
                datos[2] = autor  # Actualizar el autor del libro en la línea
                lineas[i] = ",".join(datos) + "\n"  # Unir los elementos de la lista en una cadena separada por ","
                libros.writelines(lineas)  # Sobrescribir el archivo con las líneas actualizadas
                print("Libro modificado correctamente")  
                return  
        else:
            print("Libro no encontrado")  


def eliminar_libro():  # Eliminar un libro 
    isbn = validar("isbn",13)  

    with open("libros.txt", "r+", encoding='utf-8') as libros:  # Abrir el archivo "libros.txt" en modo lectura y escritura
        lineas = libros.readlines()  # Leer todas las líneas del archivo
        libros.seek(0)  # Posicionar el puntero al inicio del archivo
        for i, linea in enumerate(lineas):  # Iterar sobre cada línea del archivo con su índice
            datos = linea.strip().split(",")  # Dividir la línea en una lista de elementos separados por ","
            if datos[0] == isbn:  #si coincide con el isbn recien ahi valido el estado
                estado=validarBajaLibro(datos[0])
                if estado==True: #si esta libre procedo a eliminarlo
                   lineas.pop(i)  # Eliminar la línea del libro
                   libros.truncate(0)  # Vaciar el contenido del archivo
                   libros.writelines(lineas)  # Sobrescribir el archivo con las líneas actualizadas
                   print("Libro eliminado correctamente")  
                   return 
                elif estado==False: #si esta prestado muestro el mensaje
                    print("No se puede eliminar el libro porque esta prestado")
                    return
        else:
            print("Libro no encontrado")  


def main():# Logica del funcionamiento del programa a traves del menu/sub menus 
    menuClientes="menuClientes.txt"
    menuLibros="menuLibros.txt"
    menuPrincipal="menu_principal.txt"
    menuPrestamos="menu_prestamos.txt"
    
    while True:
        
        mostrarMenuLindo(menuPrincipal)  # Mostrar el menú principal
        opcion = input("Seleccione una opción: ") 
        limpiarPantalla()
        if opcion == "0":
            
            consultar_disponibilidad()  
        elif opcion == "1":
            
            while True:
               
                mostrarMenuLindo(menuPrestamos)

                sub_opcion = input("Seleccione una opción: ").upper()  

                if sub_opcion == "A":
                    limpiarPantalla()
                    consultar_titulos_disponibles()  
                elif sub_opcion == "B":
                    limpiarPantalla()
                    registrar_prestamo()  
                elif sub_opcion == "C":
                    limpiarPantalla()
                    registrar_devolucion()  
                elif sub_opcion == "D":
                    limpiarPantalla()
                    break  
                else:
                    print("Opción inválida. Intente nuevamente.") 
               
        elif opcion == "2":
            limpiarPantalla()
            while True:
                
                mostrarMenuLindo(menuClientes)

                sub_opcion = input("Seleccione una opción: ").upper()

                if sub_opcion == "A":
                    limpiarPantalla()
                    alta_cliente()
                elif sub_opcion == "C":
                    limpiarPantalla()
                    consultar_estado_cliente()
                elif sub_opcion == "M":
                    limpiarPantalla()
                    modificar_cliente()
                elif sub_opcion == "E":
                    limpiarPantalla()
                    eliminar_cliente()
                elif sub_opcion == "R":
                    limpiarPantalla()
                    break
                else:
                    print("Opción inválida")
               
        elif opcion == "3":
            limpiarPantalla()
            while True:
                mostrarMenuLindo(menuLibros)

                sub_opcion = input("Seleccione una opción: ").upper()

                if sub_opcion == "A":
                    limpiarPantalla()
                    alta_libro()
                elif sub_opcion == "C":
                    limpiarPantalla()
                    consultar_libro()
                elif sub_opcion == "M":
                    limpiarPantalla()
                    modificar_libro()
                elif sub_opcion == "E":
                    limpiarPantalla()
                    eliminar_libro()
                elif sub_opcion == "R":
                    limpiarPantalla()
                    break
                else:
                    print("Opción inválida")
           
        elif opcion == "4":
            salir()
        else:
            print("Opción inválida")

      

if __name__ == "__main__":# Inicio del programa
    main() 