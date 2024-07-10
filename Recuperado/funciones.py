import os
import json
from datetime import datetime, date
from validaciones import *
     
id_auto_incremental = 0
numero_reporte = 0
lista_proyectos= []

def clear():
    '''limpia consola'''
    print()
    os.system("cls")

def cantidad_proyectos_activos(lista_proyectos:list)-> int:
    '''parametro lista con diccionarios, cuenta y retorna la cantidad de proyectos con 'estado' 'activo' '''
    contador = 0
    for proyecto in lista_proyectos:
        if (proyecto['Estado'] == 'Activo'):
            contador += 1
    return contador        

def incrementar_id()-> int:
    '''incrementa el global id_auto_incremental y lo retorna el valor'''
    global id_auto_incremental
    id_auto_incremental +=1
    return id_auto_incremental

def decrementar_id()-> int:
    '''decrementa el global id_auto_incremental y retorna el valor'''
    global id_auto_incremental
    id_auto_incremental -=1
    return id_auto_incremental     

def parse_csv(nombre_archivo:str)-> list:
    '''Por parametro el archivo.csv y retorna en formato de lista con diccionarios individuales dentro, además verifica que el csv no cuente con 50 archivos activos'''
    lista_elementos = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo,"r",encoding='utf-8') as archivo:
            primer_linea = archivo.readline().strip()
            primer_linea = primer_linea.replace("\n","")
            lista_claves = primer_linea.split(",")

            for linea in archivo:
                linea_aux = linea.replace("\n","")
                lista_valores = linea_aux.split(",")
                diccionario_aux = {}

                for i in range(len(lista_claves)):
                    diccionario_aux[lista_claves[i]] = lista_valores[i]
                
                if (diccionario_aux['Estado'] == 'Activo' and cantidad_proyectos_activos(lista_elementos) >= 50):
                    print("Con este set de datos ingresado no se puede iniciar el programa, ya que tiene más de 50 proyectos activos")
                else:
                    lista_elementos.append(diccionario_aux)
                    incrementar_id()
        return lista_elementos  
    else:
        print("Error. El archivo no existe.")

def parsear_fecha(fecha_str:str, formato="%d-%m-%Y")-> date:
    '''Convierte un string de fecha ("DD-MM-AAAA") a un objeto datetime.'''
    fecha = datetime.strptime(fecha_str, formato).date()
    return fecha

def normalizar_datos(proyectos:list) -> str:
    '''Por parámetro lista con bibliotecas, convierte datos presupuesto-> int, fecha inicio y fecha fin -> date. retorna mensaje si efectuó cambios o no'''
    modificacion = False
    mensaje = "Hubo un error al normalizar los datos. Verifique que la lista no este vacía o que los datos ya no se hayan normalizado anteriormente"
    for proyecto in proyectos:
        for clave in proyecto:
            valor = proyecto[clave]
            if clave.lower() == "id" or clave.lower() == "presupuesto":
                proyecto[clave] = int(valor)
                modificacion = True
            elif clave == "Fecha de inicio" or clave == "Fecha de Fin":
                fecha = proyecto[clave]
                proyecto[clave] = parsear_fecha(fecha)
                modificacion = True
    if modificacion:
        mensaje = "Datos Normalizados"
    return mensaje

lista_proyectos = parse_csv("Proyectos.csv") 
normalizar_datos(lista_proyectos)

def normalizar_datos_export(proyectos:list) -> str:
    '''Por parámetro lista con bibliotecas, convierte datos presupuesto, fecha inicio y fecha fin -> String. retorna mensaje si efectuó cambios o no'''
    modificacion = False
    mensaje = "Hubo un error al normalizar los datos. Verifique que la lista no este vacía o que los datos ya no se hayan normalizado anteriormente"
    
    for proyecto in proyectos:
        if isinstance(proyecto['id'], int):
            proyecto['id'] = str(proyecto['id'])
            modificacion = True    
        if isinstance(proyecto['Presupuesto'], int):
            proyecto['Presupuesto'] = str(proyecto['Presupuesto'])
            modificacion = True 
        if isinstance(proyecto['Fecha de inicio'], date):
            fecha = proyecto['Fecha de inicio']
            fecha = fecha.strftime("%d-%m-%Y")
            proyecto['Fecha de inicio'] = str(fecha)
            modificacion = True
        if isinstance(proyecto['Fecha de Fin'], date):
            fecha = proyecto['Fecha de Fin']
            fecha = fecha.strftime("%d-%m-%Y")
            proyecto['Fecha de Fin'] = str(fecha)
            modificacion = True
    if modificacion:
        mensaje = "Datos Normalizados"

    return mensaje

def generar_json(nombre_archivo: str, lista: list):
    '''Param Nombre del archivo a escribir y lista que se ingresará'''
    with open(nombre_archivo, "w",encoding='utf-8') as archivo:
        json.dump(lista, archivo, indent = 4)

def generar_csv(nombre_archivo: str,lista: list):
    '''Param nombre del archivo y lista, en caso que la lista no esté vacia escribe/sobreescribe el csv'''
    if len(lista) > 0:
        lista_keys = list(lista[0].keys())
        primera_linea = ",".join(lista_keys)
        with open(nombre_archivo, "w") as archivo:
            archivo.write(primera_linea + "\n")
            for proyecto in lista:
                lista_valores = list(proyecto.values())
                for i in range(len(lista_valores)):
                    lista_valores[i] = str(lista_valores[i])
                dato = ",".join(lista_valores)
                dato += "\n"
                archivo.write(dato)
    else:
        print("ERROR: Lista vacía.")

#Funciones de ingresos
def ingresar_nombre()-> str: 
    '''Ingreso de nombre por input, validacion y retorna el nombre del proyecto, en caso de no completar, retorna "ERROR" '''
    nombre = input("Ingrese el nombre del proyecto: ")
    while (validar_nombre(nombre) == False):
        if (reingreso_dato_error()):
            nombre = input("Reingrese el nombre del proyecto: ")
        else:
            nombre = "ERROR"
            break
    return nombre                

def ingresar_descripcion()-> str: 
    '''Solicita la descripcion, valida y retorna la misma, en caso de no completar, retorna "ERROR" '''
    descripcion = input("Ingrese la descripción: ")
    while (validar_descripcion(descripcion) == False):
        if (reingreso_dato_error()):
            descripcion = input("Reingrese la descripción: ")
        else:
            descripcion = "ERROR"
            break
    return descripcion 

def ingresar_presupuesto()-> int: 
    '''solicita el de nombre, valida y retorna el presupuesto,  en caso de no completar, retorna "ERROR" '''
    presupuesto = int(input("Ingrese el presupuesto: "))
    while (validar_presupuesto(presupuesto) == False):
        if (reingreso_dato_error()):
            presupuesto = int(input("Reingrese el presupuesto: "))
        else:
            presupuesto = "ERROR"
            break
    return presupuesto  

def ingresar_fecha_inicio() -> date: 
    '''Solicita la fecha, se valida y se retorna la misma en datetime, en caso de no completar, retorna "ERROR" '''
    fecha = input(f"Ingrese la fecha de Inicio (DD-MM-AAAA): ")
    while (validar_fecha(fecha) == False):
        if reingreso_dato_error():
            fecha = input(f"Reingrese la fecha de Inicio (DD-MM-AAAA): ")
        else:
            fecha = "ERROR"
            break

    if (fecha != "ERROR"):
        fecha = parsear_fecha(fecha)
        return fecha
    else:
        return "ERROR"
    
def ingresar_fecha_fin() -> date: 
    '''modo (inicio o fin), Solicita la fecha, se valida y se retorna la misma en datetime, en caso de no completar, retorna "ERROR" '''
    fecha = input(f"Ingrese la fecha de Fin (DD-MM-AAAA): ")
    while (validar_fecha(fecha) == False):
        if reingreso_dato_error():
            fecha = input(f"Reingrese la fecha de Fin (DD-MM-AAAA): ")
        else:
            fecha = "ERROR"
            break   

    if (fecha != "ERROR"):
        fecha = parsear_fecha(fecha)
        return fecha
    else:
        return "ERROR"
    
def crear_estado()-> str:  
    estado = "Activo"
    #El estado debe de iniciar como ‘Activo’, pudiendo ser tambien ‘Cancelado’
    modificacion = input(f"El estado está en 'Activo', desea modificarlo? (Y or any key to quit)").upper()
    if (modificacion == "Y"):
        estado = input("Ingrese el estado (Activo/Cancelado/Finalizado): ")
        while (validar_estado(estado) == False):
            if (reingreso_dato_error()):
                estado = input("Ingrese el estado (Activo/Cancelado/Finalizado): ")
            else:
                estado = "activo"
                break
    return estado.capitalize()

def ingresar_modo()-> str:
    '''Se ingresa un orden (Ascendente o Descendente), si se ingresa algo distinto a esto retorna "ERROR"'''
    modo = input('Ingrese el tipo de orden ("Ascendente/Descendente"): ')
    modo = modo.lower()  
    if (modo != 'ascendente' and modo != 'descendente'):
        return 'ERROR'
    return modo

def modificar_estado(proyecto:list)-> str:
    '''Lista con dict por parametro, id del proyecto a modificar, y retorna el valor del estado, modificado o sin modificar'''
    estado = proyecto['Estado']
    #Dentro de la lista, accedo con el id proyecto a el diccionario particular y tomo con .get() el value de la key que busco.
    modificacion = input(f"El estado está en '{estado}', desea modificarlo? (Y or any key to quit)").upper()
    if (modificacion == "Y"):
        estado = input("Ingrese el estado (Activo/Cancelado): ")
        while (validar_estado(estado) == False):
            if (reingreso_dato_error()):
                estado = input("Ingrese el estado (Activo/Cancelado): ")
            else:
                estado = "activo"
                break  
    return estado

def cargar_nuevo_proyecto(id, nombre,descripcion,fecha_inicio,fecha_fin,presupuesto,estado): 
    '''Funcion para cargar los datos del proyecto en un diccionario y agregarlo en la lista_proyectos'''
    proyecto = {
        'id':id,
        'Nombre del Proyecto':nombre,
        'Descripcion':descripcion,
        'Fecha de inicio':fecha_inicio,
        'Fecha de Fin':fecha_fin,
        'Presupuesto':presupuesto,
        'Estado':estado
    }
    lista_proyectos.append(proyecto)

def ingresar_proyecto()-> str: 
    '''Se ingresan los datos del proyecto y retorna string del resultado, si se pudo ingresar el proyecto o no.'''
    nombre = ingresar_nombre()
    descripcion = ingresar_descripcion()
    fecha_inicio = ingresar_fecha_inicio()
    fecha_fin = ingresar_fecha_fin()
    while(validar_fecha_fin(fecha_inicio,fecha_fin) == "ERROR"):
        print("ERROR, la fecha de fin es previa a la de inicio. ")
        fecha_inicio = ingresar_fecha_inicio()
        fecha_fin = ingresar_fecha_fin()
    presupuesto = ingresar_presupuesto()
    estado = crear_estado()

    if (nombre == "ERROR" or descripcion == "ERROR" or fecha_inicio == "ERROR" or fecha_fin == "ERROR" or presupuesto == "ERROR"):
        resultado = "No se pudo ingresar el proyecto, algún dato quedó incorrecto"
    elif (cantidad_proyectos_activos(lista_proyectos) < 49): # 0 - 48
        incrementar_id()
        cargar_nuevo_proyecto(id_auto_incremental,nombre,descripcion,fecha_inicio,fecha_fin,presupuesto,estado)
        resultado = "Proyecto ingresado con suceso!"
    elif(cantidad_proyectos_activos(lista_proyectos) == 49): #49
        incrementar_id()
        cargar_nuevo_proyecto(id_auto_incremental,nombre,descripcion,fecha_inicio,fecha_fin,presupuesto,estado)
        print("El programa cuenta con este ingreso un total de 49 Proyectos activos.")
        resultado = "Proyecto ingresado con suceso!"
    else: #50 o más
        print("El programa ya cuenta con 50 proyectos.")
        resultado = "ERROR"
    return resultado

def obtener_proyecto_por_id(lista_proyectos:list, id_buscado:int):
    '''Parametro lista de diccionarios, buscamos diccionario por id y retornamos el mismo completo, en caso de no encontrar retorna "ERROR" '''
    for proyecto in lista_proyectos:
        if (proyecto['id'] == id_buscado):
            return proyecto           
    return "ERROR"

def convertir_fecha_a_string(fecha):
    '''Param fecha, convierte a str y retorna'''
    fecha = fecha.strftime("%d/%m/%Y")
    return fecha

def mostrar_todos_proyectos(lista_proyectos:list): 
    informacion = "|    Nombre del Proyecto    |    Descripción    |    Fecha de Inicio    |    Fecha de Fin    |    Presupuesto    |    Estado    |\n"
    for proyecto in lista_proyectos:
        for clave in proyecto:
            if (clave == 'Presupuesto'):
                dato = str(proyecto[clave]).replace('"', '')
                informacion += "$" + str(dato) + " | "
            elif(clave == 'Fecha de inicio' or clave == 'Fecha de Fin'):
                dato = proyecto[clave]
                informacion += str(dato.strftime("%d-%m-%Y")) + " | "                
            elif (clave != 'id'):
                informacion += str(proyecto[clave]) + " | "
        informacion += "\n"            
    print(informacion)

def mostrar_todos_proyectos_con_id(lista_proyectos:list): 
    informacion = "| ID |    Nombre del Proyecto    |    Descripción    |    Fecha de Inicio    |    Fecha de Fin    |    Presupuesto    |    Estado    |\n"
    for proyecto in lista_proyectos:
        for clave in proyecto:
            if (clave == 'id'):
                dato = proyecto['id']
                informacion += str(dato) + " | "
            elif (clave == 'Presupuesto'):
                dato = proyecto['Presupuesto']
                informacion += "$" + str(dato) + " | "
            elif(clave == 'Fecha de inicio' or clave == 'Fecha de Fin'):
                dato = proyecto[clave]
                informacion += str(dato.strftime("%d-%m-%Y")) + " | " 
            else:
                informacion += str(proyecto[clave]) + " | "
        informacion += "\n"            
    print(informacion)    

def mostrar_proyecto_individual(proyecto:list):
    informacion = "| ID |    Nombre del Proyecto    |    Descripción    |    Fecha de Inicio    |    Fecha de Fin    |    Presupuesto    |    Estado    |\n"
    for clave in proyecto:
        if (clave == 'id'):
            dato = proyecto['id']
            informacion += str(dato) + " | "
        elif (clave == 'Presupuesto'):
            dato = proyecto['Presupuesto']
            informacion += "$" + str(dato) + " | "
        elif(clave == 'Fecha de inicio' or clave == 'Fecha de Fin'):
            dato = proyecto[clave]
            informacion += str(dato.strftime("%d-%m-%Y")) + " | " 
        else:
            informacion += str(proyecto[clave]) + " | "
    informacion += "\n"            
    print(informacion)

def modificar_dato_proyecto(proyecto:dict, key:str, dato)-> bool: 
    '''Param lista con diccionario dentro, key a modificar y dato a ingresar, mensaje de éxito con retorna True o mensaje de fallo con return False'''
    #Esta funcion parece peligrosa pero nunca se accede a ella como usuario, es decir siempre está concatenada a otras funciones que validan sus datos
    if (dato != "ERROR"):
        proyecto[key] = dato
        print("El dato se ha modificado con éxito")
        return True
    else:
        print("No se ha podido modificar el dato: Dato erroneo")
        return False
    
def imprimir_submenu_modificacion_proyecto(): 
    '''print de submenu de modificacion de proyecto'''
    print("\nOpciones de modificacion ")
    print("1. Nombre del Proyecto")
    print("2. Descripción del Proyecto")
    print("3. Presupuesto del Proyecto")
    print("4. Fecha de inicio del Proyecto")
    print("5. Fecha de Fin del Proyecto")
    print("6. Estado del Proyecto")
    print("7. Volver al menú anterior")

def switch_variable_bool(switch:bool, variable_bool_cambiar:bool): 
    '''param bool True cambia la variable ingresada(true a false, y viceversa)'''
    if (switch == True):
        if(variable_bool_cambiar == False):
            variable_bool_cambiar = True

def modificar_proyecto(lista_proyectos:list)-> str: 
    '''La lista de proyectos, se pedirá el id_proyecto (se valida).Luego un submenu de opciones (Datos a modificar), retorna mensaje si hubo cambios o no.'''
    hubo_cambio_exitoso = False
    mensaje = "No se realizaron modificaciones"
    mostrar_todos_proyectos_con_id(lista_proyectos)
    id_proyecto = int(input('Ingrese el id del proyecto a modificar: '))
    proyecto = obtener_proyecto_por_id(lista_proyectos, id_proyecto)

    if (proyecto != "ERROR"):
            while(True):
                imprimir_submenu_modificacion_proyecto()
                opcion = int(input("Seleccione la opcion: "))
                match (opcion):
                    case 1:
                        clear()
                        nombre = ingresar_nombre()
                        resultado = modificar_dato_proyecto(proyecto,'Nombre del Proyecto', nombre)
                        hubo_cambio_exitoso = switch_variable_bool(resultado, hubo_cambio_exitoso)
                        mostrar_proyecto_individual(proyecto)
                    case 2:
                        clear()
                        descripcion = ingresar_descripcion()
                        resultado = modificar_dato_proyecto(proyecto,'Descripcion', descripcion)
                        hubo_cambio_exitoso = switch_variable_bool(resultado, hubo_cambio_exitoso)
                        mostrar_proyecto_individual(proyecto)
                    case 3:
                        clear()
                        presupuesto = ingresar_presupuesto()
                        resultado = modificar_dato_proyecto(proyecto,'Presupuesto', presupuesto)
                        hubo_cambio_exitoso = switch_variable_bool(resultado, hubo_cambio_exitoso)
                        mostrar_proyecto_individual(proyecto)
                    case 4:
                        clear()
                        fecha_inicio = ingresar_fecha_inicio()
                        resultado = modificar_dato_proyecto(proyecto,'Fecha de inicio', fecha_inicio)
                        hubo_cambio_exitoso = switch_variable_bool(resultado, hubo_cambio_exitoso)
                        mostrar_proyecto_individual(proyecto)
                    case 5:
                        clear()
                        fecha_inicio = proyecto.get('Fecha de inicio')
                        fecha_fin = ingresar_fecha_fin()
                        if(fecha_fin > fecha_inicio):
                            resultado = modificar_dato_proyecto(proyecto,'Fecha de Fin', fecha_fin)
                            hubo_cambio_exitoso = switch_variable_bool(resultado, hubo_cambio_exitoso)         
                            mostrar_proyecto_individual(proyecto)
                        else:
                            print("ERROR: No se pudieron realizar los cambios, error de fecha")
                    case 6:
                        clear()
                        estado = modificar_estado(proyecto)
                        resultado = modificar_dato_proyecto(proyecto,'Estado', estado)
                        hubo_cambio_exitoso = switch_variable_bool(resultado, hubo_cambio_exitoso)
                        mostrar_proyecto_individual(proyecto)
                    case _:
                        clear()
                        if (hubo_cambio_exitoso == False):
                            print(mensaje)
                        print('Volviendo al menú principal... \n')
                        break
    else:
        mensaje = 'DATA ERROR: Proyecto por id no encontrado'
        print(mensaje)
        print('Volviendo al menú principal... \n')

def cancelar_proyecto(lista_proyectos:list)-> str: 
    '''Lista de proyectos, se ingresa el id (se valida) y la funcion altera el estado a 'Cancelado'. Sino ERROR'''
    mostrar_todos_proyectos_con_id(lista_proyectos)
    id_proyecto = int(input('Ingrese el id del proyecto a cancelar: '))
    proyecto = obtener_proyecto_por_id(lista_proyectos, id_proyecto)
    if (proyecto != "ERROR"):
        if(proyecto['Estado'] != 'Cancelado'):
            proyecto['Estado'] = 'Cancelado'
            print(f"El proyecto id {id_proyecto} ha sido cancelado")
        else:
            print("ERROR: Proyecto ya se encuentra cancelado") 
    else:
        print("ERROR: No se encuentra un proyecto con este id")                   

def comprobar_finalizados_por_fecha_proyectos(lista_proyectos: list):
    '''Lista con diccionarios, revisa que si el día de la fecha es mayor a el día de fin para actualizar el estado de 'Activo' a 'Finalizado' '''
    for proyecto in lista_proyectos:
        fecha_fin = proyecto['Fecha de Fin']
        if (proyecto['Estado'] == 'Activo' and fecha_fin < date.today()):
            proyecto['Estado'] = 'Finalizado'
            id = proyecto['id']
            modificaciones = f'El proyecto de id {id} se encuentra finalizado, su fecha de fin ya pasó'
            print(modificaciones)

    print('Todos los proyectos están en sus estados correctos.')                   

def calcular_presupuesto_promedio(lista_proyectos:list): 
    suma_presupuesto = 0
    cantidad_proyectos = 0
    for proyecto in lista_proyectos:
        for clave in proyecto:
            if(clave == 'Presupuesto'):
                dato = proyecto['Presupuesto']
                suma_presupuesto += dato
                cantidad_proyectos += 1

    resultado = suma_presupuesto / cantidad_proyectos
    resultado = int(resultado)
    print (f'El promedio de presupuesto de todos los proyectos es ${resultado}')  

def buscar_proyecto_por_nombre(lista_proyectos:list): 
    '''Param lista con diccionarios, se ingresa nombre de proyecto a buscarse y se retorna. Sino ERROR'''
    nombre_proyecto = ingresar_nombre()
    informacion = "ERROR: No se ha encontrado ningún proyecto con este nombre en la lista de proyectos"
    if (nombre_proyecto != "ERROR"):
        for proyecto in lista_proyectos:
            if (proyecto['Nombre del Proyecto'] == nombre_proyecto):
                informacion = "|    Nombre del Proyecto    |    Descripción    |    Fecha de Inicio    |    Fecha de Fin    |    Presupuesto    |    Estado    |\n"
                #en la variable "claves" obtengo todas las claves menos la primera (index 0).
                claves = list(proyecto.keys())[1:]
                for clave in claves:
                    informacion += str(proyecto[clave]) + " | "

    print(informacion)      

def ordenar_proyectos(lista_proyectos:list): 
    '''Lista con diccionarios dentro, dato a ordenar, y modo Ascendente (True) o Descendente (False)'''
    key_a_ordenar = input('Ingrese la key a ordenar(Nombre del proyecto, Presupuesto o Fecha de inicio) : ')
    resultado = validar_key_ordenable(key_a_ordenar)

    lista_aux = lista_proyectos[:] #Creo una copia de la lista, no la sobreescribo

    while (resultado == False):
        if (reingreso_dato_error()):
            key_a_ordenar = input('Ingrese la key a ordenar(Nombre del proyecto, Presupuesto o Fecha de inicio) : ')
            resultado = validar_key_ordenable(key_a_ordenar)
        else:
            key_a_ordenar == "ERROR"
            break

    modo = ingresar_modo()
    while(modo == "ERROR"):
        if (reingreso_dato_error()):
            modo = ingresar_modo()
        else:
            modo == "ERROR"
            break

    match(key_a_ordenar.lower()):
        case 'nombre del proyecto':
            key_a_ordenar = 'Nombre del Proyecto'
        case 'presupuesto':
            key_a_ordenar = 'Presupuesto'
        case 'fecha de inicio':
            key_a_ordenar = 'Fecha de inicio'                        

    if(key_a_ordenar in ("Nombre del Proyecto", "Presupuesto", "Fecha de inicio")):
        if(modo in ('ascendente', 'descendente')):
            #ORDENAMIENTO
            if (key_a_ordenar == 'Nombre del Proyecto' or key_a_ordenar == 'Presupuesto' or key_a_ordenar == 'Fecha de inicio'):
                if (modo == 'ascendente'): 
                    for i in range(len(lista_aux)):
                        for j in range(i+1, len(lista_aux)):
                            if lista_aux[i].get(key_a_ordenar) > lista_aux[j].get(key_a_ordenar):
                                aux = lista_aux[i]
                                lista_aux[i] = lista_aux[j]
                                lista_aux[j] = aux   
                elif(modo == 'descendente'):
                    for i in range(len(lista_aux)):
                        for j in range(i+1, len(lista_aux)):
                            if lista_aux[i].get(key_a_ordenar) < lista_aux[j].get(key_a_ordenar):
                                aux = lista_aux[i]
                                lista_aux[i] = lista_aux[j]
                                lista_aux[j] = aux 
        else:
            print('Se canceló la opción de ordenar los proyectos!')
    else:
        print('ERROR: Su clave no es una de las claves válidas ("Nombre del Proyecto", "Presupuesto" o "Fecha de inicio)')
        if (reingreso_dato_error()):
            ordenar_proyectos(lista_proyectos)
        else:
            print('Se canceló la opción de ordenar los proyectos! ')  
    print()
    mostrar_todos_proyectos(lista_aux)                           

def retomar_proyecto(lista_proyectos:list):      
    mostrar_todos_proyectos_con_id(lista_proyectos)   
    id_buscado = int(input('Ingrese el id del proyecto a retomar: '))
    proyecto = obtener_proyecto_por_id(lista_proyectos,id_buscado)

    if  (proyecto == "ERROR"):
        print("ERROR: No se ha encontrado un proyecto con este ID!")
    else:
        if(proyecto['Estado'] != 'Cancelado'):
            print("ERROR: No podemos retomar este proyecto ya que no se encuentra deshabilitado!")
        else:
            fecha_fin = proyecto['Fecha de Fin']
            if(fecha_fin < date.today()):
                print('No se puede dar de alta ya que el proyecto caducó')
            else:
                proyecto['Estado'] = 'Activo'
                print(f'SUCESS: El Proyecto de id {id_buscado} se encuentra nuevamente Activo!')                                 

def reporte_por_presupuesto(lista_proyectos:list):
    '''Ingresar el presupuesto, todos los proyectos por encima del mismo se reportarán en .txt'''
    presupuesto_ingresado = ingresar_presupuesto()
    lista_proyectos_reportados = []

    if(presupuesto_ingresado != "ERROR"):
        for proyecto in lista_proyectos:
            if (proyecto['Presupuesto'] > presupuesto_ingresado):
                lista_proyectos_reportados.append(proyecto)
        
        global numero_reporte
        numero_reporte += 1
        nombre_archivo = f'reporte_num_{numero_reporte}.txt'

        normalizar_datos_export(lista_proyectos_reportados)
        with open(nombre_archivo, 'w',encoding='utf-8') as archivo:
            archivo.write(f'REPORTE DE PROYECTOS con PRESUPUESTO mayor a ${presupuesto_ingresado} \n')
            archivo.write("\n") #Espacio
            archivo.write(f'Proyecto | Fecha de Inicio | Fecha de Fin | Presupuest | Estado\n')
            for proyecto in lista_proyectos_reportados:
                nombre = proyecto['Nombre del Proyecto']
                fecha_inicio = proyecto['Fecha de inicio']
                fecha_fin = proyecto['Fecha de Fin']
                presupuesto = proyecto['Presupuesto']
                estado = proyecto['Estado']
                archivo.write(f'{nombre} | {fecha_inicio} | {fecha_fin} | ${presupuesto} | {estado} \n')
    else:
        print('ERROR: No se ha realizado ningún reporte, el presupuesto es inválido.')    

def reporte_por_nombre(lista_proyectos:list):
    '''Ingresar el nombre, todos los proyectos con el mismo se reportarán en .txt'''
    nombre = ingresar_nombre()
    lista_proyecto_reportado = []

    if(nombre != "ERROR"):
        for proyecto in lista_proyectos:
            if (proyecto['Nombre del Proyecto'] == nombre):
                lista_proyecto_reportado.append(proyecto)

        global numero_reporte
        numero_reporte += 1
        nombre_archivo = f'reporte_num_{numero_reporte}.txt'

        normalizar_datos_export(lista_proyecto_reportado)
        with open(nombre_archivo, 'w',encoding='utf-8') as archivo:
            archivo.write(f'REPORTE DE PROYECTOS "{nombre}" \n')
            archivo.write("\n") #Espacio
            archivo.write(f'Proyecto | Fecha de Inicio | Fecha de Fin | Presupuest | Estado\n')
            for proyecto in lista_proyecto_reportado:
                nombre = proyecto['Nombre del Proyecto']
                fecha_inicio = proyecto['Fecha de inicio']
                fecha_fin = proyecto['Fecha de Fin']
                presupuesto = proyecto['Presupuesto']
                estado = proyecto['Estado']
                archivo.write(f'{nombre} | {fecha_inicio} | {fecha_fin} | {presupuesto} | {estado} \n')
    else:
        print('ERROR: No se ha realizado ningún reporte, el nombre es inválido.')   

def exportar_lista_proyectos_al_csv(nombre_archivo: str,lista_proyectos: list):
    if len(lista_proyectos) > 0:
        lista_claves = list(lista_proyectos[0].keys())
        cabecera = ",".join(lista_claves)

        with open(nombre_archivo, "w",encoding='utf-8') as archivo:
            archivo.write(cabecera + "\n")
            for proyecto in lista_proyectos:
                lista_valores = list(proyecto.values())
                for i in range(len(lista_valores)):
                    # Paso los valores a string ya que el join sino es str no me deja separarlos
                    lista_valores[i] = str(lista_valores[i])
                dato = ",".join(lista_valores)
                dato += "\n"
                archivo.write(dato)
    else:
        print("Error, lista vacía")                         

def imprimir_menu_principal(): 
    print("\nSeleccione una opción:")
    print("1. Ingresar proyecto") 
    print("2. Modificar proyecto") 
    print("3. Cancelar proyecto") 
    print("4. Comprobar proyectos") 
    print("5. Mostrar todos los proyectos") 
    print("6. Calcular presupuesto promedio") 
    print("7. Buscar proyecto por nombre") 
    print("8. Ordenar proyectos") 
    print("9. Retomar proyecto") 
    print("10. Reporte por Presupuesto") 
    print("11. Reporte por Nombre de Proyecto") 
    print("12. Calcula presupuesto promedio en proyectos que duraron como mínimo 2 años") 
    print("13. Mostrar proyectos terminados en temporada de cuarentena de COVID.19") 
    print("Otro. Salir") 

def generar_json_proyectos_terminados(lista_proyectos):
    lista_proyectos_terminados = []
    lista_aux = lista_proyectos[:]
    normalizar_datos_export(lista_aux)
    for proyecto in lista_aux:
        if (proyecto['Estado'] == "Finalizado"):
            lista_proyectos_terminados.append(proyecto)
    generar_json('ProyectosTerminados.json', lista_proyectos_terminados)

def anio_proyecto(dato):
    '''Param dato de fecha en string (formato DD-MM-AAAA), retorna solamente el año'''
    dato = dato.replace("-", "")
    anio = dato[-4:]
    return anio

def calcular_presupuesto_promedio_2anios(lista_proyectos):
    '''Param lista con diccionarios, calcula el promedio de los proyectos finalizados con mas de 2 años de duración.'''
    suma_presupuesto = 0
    cantidad_proyectos = 0

    for proyecto in lista_proyectos:
        anio_inicio = (proyecto['Fecha de inicio']).year
        anio_fin = (proyecto['Fecha de Fin']).year
        diferencia = anio_fin - anio_inicio
        if (proyecto['Estado'] == 'Finalizado' and diferencia >= 2):
            cantidad_proyectos += 1
            suma_presupuesto += proyecto['Presupuesto']

    if (cantidad_proyectos > 0):
        resultado = suma_presupuesto / cantidad_proyectos
        promedio = f'El promedio de los proyectos con finalizados con más de dos años de duración es de ${resultado}'
        return promedio
    else:
        mensaje = 'No hay proyectos con esa condicion'
        return mensaje

def mostrar_proyectos_finalizados_cuarentena(lista_proyectos):
    '''Param lista con diccionarios dentro, retorna mensaje si hubo o no proyectos finalizados en tempoarada covid '''
    inicio_temporada_covid = date(2020, 3, 1)
    fin_temporada_covid = date(2021, 12, 31)
    proyectos_finalizados_en_covid = "Proyectos finalizados en covid: \n"
    bandera = False

    for proyecto in lista_proyectos:
        fecha_fin = proyecto['Fecha de Fin']
        if (inicio_temporada_covid <= fecha_fin <= fin_temporada_covid): #Si la fecha de fin es mayor al inicio y menor al fin, está dentro
            bandera = True
            for clave in proyecto:
                if (clave == 'Presupuesto'):
                    dato = str(proyecto[clave]).replace('"', '')
                    proyectos_finalizados_en_covid += "$" + str(dato) + " | "
                elif(clave == 'Fecha de inicio' or clave == 'Fecha de Fin'):
                    dato = proyecto[clave]
                    proyectos_finalizados_en_covid += str(dato.strftime("%d-%m-%Y")) + " | "                
                elif (clave != 'id'):
                    proyectos_finalizados_en_covid += str(proyecto[clave]) + " | "
            proyectos_finalizados_en_covid += "\n"         

    if (bandera == False):
        proyectos_finalizados_en_covid = "No hubo proyectos finalizados en temporada de covid"        

    return proyectos_finalizados_en_covid