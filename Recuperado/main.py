from funciones import *

while(True):
    imprimir_menu_principal()
    opcion = int(input("Seleccione la opcion: "))
    match(opcion):
        case 1:
            clear()
            ingresar_proyecto()
        case 2:
            clear()
            modificar_proyecto(lista_proyectos)        
        case 3:
            clear()
            cancelar_proyecto(lista_proyectos)
        case 4:
            clear()
            comprobar_finalizados_por_fecha_proyectos(lista_proyectos) 
        case 5:
            clear()
            mostrar_todos_proyectos(lista_proyectos)
        case 6:
            clear()
            calcular_presupuesto_promedio(lista_proyectos)
        case 7:
            clear()
            buscar_proyecto_por_nombre(lista_proyectos)
        case 8:
            clear()
            ordenar_proyectos(lista_proyectos)
        case 9:
            clear()
            retomar_proyecto(lista_proyectos)
        case 10:
            clear()
            reporte_por_presupuesto(lista_proyectos)
        case 11:
            clear()
            reporte_por_nombre(lista_proyectos)
        case 12:
            clear()
            print(calcular_presupuesto_promedio_2anios(lista_proyectos))
        case 13:
            clear()
            print(mostrar_proyectos_finalizados_cuarentena(lista_proyectos))
        case _:
            clear()
            generar_json_proyectos_terminados(lista_proyectos)
            exportar_lista_proyectos_al_csv("Proyectos.csv", lista_proyectos)
            print('Saliendo... Gracias!')
            break                                                                                