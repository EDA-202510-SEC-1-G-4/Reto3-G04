import time
import csv
from datetime import datetime as dt
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import single_linked_list as sl
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import map_functions as mf
import os



csv.field_size_limit(2147483647)
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
   
    catalog = {}
    
    catalog['ID'] = {'data': rbt.new_map(), 'size': 0} #DR_NO
    catalog['Date_Rptd'] = {'data': rbt.new_map(), 'size': 0} #Fecha en que se reporto el crimen
    catalog["Date_Occrd"] = {'data': rbt.new_map(), 'size': 0} #Fecha en que ocurrio el crimen
    catalog['Area'] = {'data': mp.new_map(10000), 'size': 0} #Nombre del area
    catalog['Edad'] = {'data': rbt.new_map(), 'size': 0} #Victim Age
    catalog['Codigos'] = {'data': rbt.new_map(), 'size': 0}
    
    
    catalog['filas'] = al.new_list()
    
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    retorno = ''
    agfile = data_dir + filename
    file = open(agfile, 'r', encoding='utf-8')
    filas = csv.DictReader(file)

    reportes = al.new_list()
    for fila in filas:
        fila["Date Rptd"] = dt.strptime(fila["Date Rptd"], '%m/%d/%Y %I:%M:%S %p')
        fila["DATE OCC"] = dt.strptime(fila["DATE OCC"], '%m/%d/%Y %I:%M:%S %p')
        al.add_last(reportes,fila)
   
    for fila in reportes["elements"]:
        
        #Identificador unico de crimen
        rbt.put(catalog["ID"]["data"],fila["DR_NO"],fila)
        catalog["ID"]["size"] += 1

        #Fecha en la que se reporto el crimen:
        exist = rbt.get(catalog['Date_Rptd']['data'],fila["Date Rptd"])
        add_rbt(catalog['Date_Rptd']['data'],fila["Date Rptd"])
        catalog["Date_Rptd"]["size"] += 1

        #Fecha en la que ocurrio el crimen:
        exist = rbt.get(catalog['Date_Occrd']['data'],fila["DATE OCC"])
        add_rbt(catalog['Date_Occrd']['data'],fila["DATE OCC"])
        catalog["Date_Occrd"]["size"] += 1

        #Areas:
        hash_value = mf.hash_value(catalog['Area']['data'],fila['AREA NAME'])
        if mp.contains(catalog['Area']['data'],fila['AREA NAME']):
            al.add_last(catalog['Area']['data']['table']['elements'][hash_value]['value'],fila)
        else:
            lista = al.new_list()
            al.add_last(lista,fila)
            mp.put(catalog["Area"]["data"],fila["AREA NAME"],lista)
        catalog["Area"]["size"] += 1


        #Edad de la victima:
        
        add_rbt(catalog['Edad']['data'],fila["Vict Age"])
        catalog["Edad"]["size"] += 1


        #Codigo del crimen:
        
        add_rbt(catalog['Codigos']['data'],fila["Crm Cd"])
        
        catalog["Codigos"]["size"] += 1

        al.add_last(catalog["filas"],fila)

    cinco = []
    for i in range(5):
        cinco.append(catalog["filas"]["elements"][i])
    for i in range(1,6):
        cinco.append(catalog["filas"]["elements"][-i])

    for fila2 in cinco:
        retorno += (f"ID: {fila2['DR_NO']}\n"
                f"Fecha reportada del crimen: {fila2['Date Rptd']}\n"
                f"Fecha en la que ocurrio el crimen: {fila2['DATE OCC']}\n"
                f"Nombre del Area: {fila2['AREA NAME']}\n"
                f"Codigo del Crimen: {fila2['Crm Cd']}\n"
                f"\n =========================== \n")
        

    return retorno

def add_rbt (tree,key):
        exist = rbt.get(tree,key)
        if exist == None:
            lista = al.new_list()
            al.add_last(lista,key)
            rbt.put(tree,key,lista)
        else:
            al.add_last(exist,key)
            rbt.put(tree,key,exist)
            
        return tree
         




def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass

def req_1(catalog, start_date, end_date):
    """
    Retorna el resultado del requerimiento 1
    """
    start_date = dt.strptime(start_date, "%Y-%m-%d")
    end_date = dt.strptime(end_date, "%Y-%m-%d")

    # Obtener los registros de crímenes (las filas con la información de cada crimen)
    filas = catalog['filas']['elements']
    
    # Lista para almacenar los crímenes que cumplen con el criterio de fechas
    crímenes_filtrados = []

    # Filtrar crímenes entre las fechas proporcionadas
    for fila in filas:
        try:
            # Formato para fecha y hora (12 horas AM/PM)
            crime_date = dt.strptime(fila["DATE OCC"], "%m/%d/%Y %I:%M:%S %p")  # Incluye AM/PM
        except ValueError:
            # Si la fecha no tiene hora, solo consideramos la fecha
            crime_date = dt.strptime(fila["DATE OCC"], "%m/%d/%Y")

        # Si el crimen ocurrió dentro del rango de fechas
        if start_date <= crime_date <= end_date:
            crímenes_filtrados.append(fila)

    # Ordenar los crímenes primero por fecha (más reciente) y luego por área en caso de empate
    crímenes_filtrados.sort(key=sort_by_date_and_area)

    # Generar la respuesta en el formato solicitado
    resultado = []
    for fila in crímenes_filtrados:
        resultado.append({
            "DR_NO": fila['DR_NO'],
            "DATE OCC": fila['DATE OCC'],
            "TIME OCC": fila['TIME OCC'],
            "AREA NAME": fila['AREA NAME'],
            "Crm Cd": fila['Crm Cd'],
            "LOCATION": fila['LOCATION']
        })

    # Retornar los resultados
    return resultado

def sort_by_date_and_area(fila):
    """
    Función auxiliar para ordenar por fecha y hora, luego por área.
    Retorna una tupla para realizar la comparación de manera explícita.
    """
    # Convertimos la fecha y la hora en objetos datetime para que puedan ser comparados
    try:
        date_obj = dt.strptime(fila["DATE OCC"], "%m/%d/%Y %I:%M:%S %p")  # Usando AM/PM
    except ValueError:
        date_obj = dt.strptime(fila["DATE OCC"], "%m/%d/%Y")  # En caso de solo fecha
    
    time_obj = fila["TIME OCC"]
    
    # Retornamos una tupla con (fecha, hora, área)
    return (date_obj, time_obj, fila["AREA NAME"])


    

def req_2(catalog,fecha_in,fecha_fin):
    """
    Retorna el resultado del requerimiento 2
    """
    retorno2 = ''
    filtro = rbt.values(catalog["Date_Rptd"]["data"],fecha_in,fecha_fin)
    filtrados = al.new_list()
    
    for i in range(sl.size(filtro)):
        fila = sl.get_element(filtro,i)
        
        if fila["Part 1-2"] == 1:
            if fila["Status"] != "IC":
                fechaHora = fila["DATE OCC"].split(" ")
                al.add_last(filtrados, fila)
    
    retorno = al.merge_sort(filtrados,compare_crit_by_date)  # O heapsort no se cual sea mejor lol
    reportes = retorno                
    if al.size(retorno) > 10:
        
        reportes = retorno["elements"][:5] + retorno["elements"][-5:]
    
    for fila in reportes:
        retorno2 += (f"ID del crimen: {fila['DR_NO']}\n"
                 f"Fecha del incidente: {fechaHora[0]}\n"
                 f"Hora del incidente: {fechaHora[1]}\n"
                 f"Área: {fila['AREA NAME']}\n"
                 f"Subárea: {fila['Sub Area']}\n"
                 f"Clasificación: Parte 2\n"
                 f"Código del crimen: {fila['Crm Cd']}\n"
                 f"Estado del caso: {fila['Status Desc']}\n"
                 f"\n===========================\n")
        
    return retorno2
                

def compare_crit_by_date(elm1,elm2):
    isSorted = False

    fecha1 = elm1["DATE OCC"]
    fecha2 = elm2["DATE OCC"]
    area1 = elm2["AREA NAME"]
    area2 = elm2["AREA NAME"]
    
    if fecha1 > fecha2:
        isSorted = True
    elif fecha1 == fecha2:
        if area1 > area2:
            isSorted = True
    
    return isSorted


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog,n_areas,fecha_in,fecha_fin):
    #Definición de variables generales:
    fecha_in = dt.strptime(fecha_in,"%Y-%m-%d")
    fecha_fin = dt.strptime(fecha_fin,"%Y-%m-%d")
    areas = catalog['Area']['data']
    
    #Primer filtro (fecha):
    

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
