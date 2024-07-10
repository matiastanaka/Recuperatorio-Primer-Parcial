from datetime import datetime, date, timedelta

def reingreso_dato_error()-> bool: 
    '''Validacion de consulta para reingreso de dato erroneo, True for Y, sino False'''
    mensaje = (input("DATO ERROR: Quiere reingresarlo? (Y or any key to quit): ")).upper()
    if (mensaje == "Y"):
        return True
    else:
        return False

def validar_entero(valor): 
    if(valor.isdigit()):
        return True
    else:
        return False    

def validar_string(cadena): 
    if (cadena.isalpha() and len(cadena)>0):
        return True
    else:
        return False
    
def validar_nombre(nombre:str)-> bool: 
    '''valida la condicion de alfabéticos y hasta 30 caracteres (TRUE) sino, False'''
    nombre_comparativo = nombre.replace(" ","")
    if (nombre_comparativo.isalpha() and len(nombre) <= 40):
        return True
    else:
        return False

def validar_descripcion(texto)-> bool: 
    '''valida si es alfanumerico y si tiene hasta 200 carácteres (TRUE) sino, False'''
    texto_comparativo = texto.replace(" ","")
    if (texto_comparativo.isalnum() and len(texto) <= 200):
        return True
    else:
        return False    

def validar_presupuesto(presupuesto)-> bool: 
    '''valida si es entero y mayor a 500000 (True) sino, False''' 
    if (presupuesto >= 500000):
        return True
    return False        

def validar_fecha(fecha:str) -> bool: 
    '''Valida que la fecha esté en el formato DD-MM-AAAA con guiones en las posiciones correctas y valores válidos para día, mes y año'''
    if (len(fecha) != 10):
        return False

    if fecha[2] != "-" or fecha[5] != "-":
        return False

    dia, mes, anio = fecha.split("-")
    if not (validar_entero(dia) and validar_entero(mes) and validar_entero(anio)):
        return False

    dia = int(dia)
    mes = int(mes)
    anio = int(anio)

    if (dia < 1 or dia > 31):
        return False

    if (mes < 1 or mes > 12):
        return False

    if (anio < 1 or anio > 2200):
        return False

    #Caso todo lo anterior se cumpla, True
    return True

def validar_fecha_fin(fecha_inicio, fecha_fin): 
    '''valida que la fecha final no sea anterior a la del inicio, se retorna la misma, en caso de no cumplir, retorna "ERROR"'''
    if(fecha_fin != "ERROR" and fecha_inicio != "ERROR"):
        if (fecha_inicio > fecha_fin):
            return "ERROR"
    return fecha_fin

def validar_estado (estado:str)-> bool: 
    '''Valida que el estado sea Activo o Cancelado'''
    estado = estado.lower()
    if (estado == "activo" or estado == "cancelado"):
        return True
    else:
        return False

def validar_id(id_proyecto)-> int: 
    '''Se pide un id y se valida que sea entero'''
    while ((validar_entero(id_proyecto) == False)):
        if (reingreso_dato_error()):
            id_proyecto = int(input('Ingrese el id del proyecto buscado: '))
        else:
            id_proyecto = "ERROR"
            break
    return id_proyecto  
      
def validar_key_ordenable(clave): 
    '''Se ingresa una clave, si es Nombre del proyecto, presupuesto o fecha de inicio = True, sino False'''
    clave = clave.lower()
    clave_aux = clave.replace(" ", "")
    resultado = validar_string(clave_aux)
    if (resultado):
        if (clave == "nombre del proyecto" or clave == "presupuesto" or clave == "fecha de inicio"):
            return True
    return False      