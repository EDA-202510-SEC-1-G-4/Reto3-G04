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
        add_rbt(catalog['Date_Rptd']['data'],fila["Date Rptd"],fila)
        catalog["Date_Rptd"]["size"] += 1

        #Fecha en la que ocurrio el crimen:
        add_rbt(catalog['Date_Occrd']['data'],fila["DATE OCC"],fila)
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
        add_rbt(catalog['Edad']['data'],fila["Vict Age"],fila)
        catalog["Edad"]["size"] += 1

        #Codigo del crimen:
        add_rbt(catalog['Codigos']['data'],fila["Crm Cd"],fila)
        
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

def add_rbt (tree,key,value):
    exist = rbt.get(tree,key)
    if exist == None:
        lista = al.new_list()
        al.add_last(lista,value)
        rbt.put(tree,key,lista)
    else:
        al.add_last(exist,value)
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
    retorno = ''
    
    # Convertir fechas de entrada a formato datetime
    start_date = fecha_a_Datetime(start_date)
    end_date = fecha_a_Datetime(end_date)
    
    # Obtener los valores (filas) en el rango de fechas
    fechas_filtradas = rbt.values(catalog["Date_Occrd"]["data"], start_date, end_date)
    
    # Lista para almacenar los crímenes que cumplen con el rango
    crímenes_filtrados = al.new_list()
    
    # Filtramos por las filas dentro del rango de fechas
    for i in range(sl.size(fechas_filtradas)):
        fila = sl.get_element(fechas_filtradas, i)
        
        for crimen in fila["elements"]:
            # Agregar crimen a la lista de filtrados
            al.add_last(crímenes_filtrados, crimen)
    
    # Ordenamos los crímenes por fecha (más reciente a más antiguo)
    crímenes_ordenados = al.merge_sort(crímenes_filtrados, compare_crit_by_date)

    # Mostrar los primeros 5 y los últimos 5 crímenes
    if al.size(crímenes_ordenados) > 10:
        crímenes_ordenados = crímenes_ordenados["elements"][:5] + crímenes_ordenados["elements"][-5:]
    
    # Formatear la salida
    for crimen in crímenes_ordenados:
        fechaHora = str(crimen["DATE OCC"]).split(" ")
        retorno += (f"ID del crimen: {crimen['DR_NO']}\n"
                    f"Fecha del incidente: {fechaHora[0]}\n"
                    f"Hora del incidente: {fechaHora[1]}\n"
                    f"Área: {crimen['AREA NAME']}\n"
                    f"Código del crimen: {crimen['Crm Cd']}\n"
                    f"Dirección: {crimen['LOCATION']}\n"
                    f"\n===========================\n")

    return retorno
    

def fecha_a_Datetime(fecha):

    return dt.strptime(fecha,"%m/%d/%Y")
    

def req_2(catalog,fecha_in,fecha_fin):
    """
    Retorna el resultado del requerimiento 2
    """
    retorno2 = ''
    fecha_in = fecha_a_Datetime(fecha_in)
    fecha_fin = fecha_a_Datetime(fecha_fin)
    
    filtro = rbt.values(catalog["Date_Rptd"]["data"],fecha_in,fecha_fin)
    filtrados = al.new_list()
    
    for i in range(sl.size(filtro)):
        elm = sl.get_element(filtro,i)
        for fila in elm["elements"]:
            if int(fila["Part 1-2"]) == 1:
                if fila["Status"] != "IC":
                    al.add_last(filtrados, fila)
    
    retorno = al.merge_sort(filtrados,compare_crit_by_date)  # O heapsort no se cual sea mejor lol
    reportes = retorno                
    if al.size(retorno) > 10:
        
        reportes = retorno["elements"][:5] + retorno["elements"][-5:]
    
    for fila in reportes:
        fechaHora = str(fila["DATE OCC"]).split(" ")
        retorno2 += (f"ID del crimen: {fila['DR_NO']}\n"
                 f"Fecha del incidente: {fechaHora[0]}\n"
                 f"Hora del incidente: {fechaHora[1]}\n"
                 f"Área: {fila['AREA NAME']}\n"
                 f"Subárea: {fila['Rpt Dist No']}\n"
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
    
    if fecha1 < fecha2:
        isSorted = True
    elif fecha1 == fecha2:
        if area1 < area2:
            isSorted = True
    
    return isSorted


def req_3(catalog, N, area_name):
    """
    Retorna el resultado del requerimiento 3
    """
    retorno = ''
    
    # Obtener la lista de crímenes para el área especificada
    crímenes_area = mp.get(catalog["Area"]["data"], area_name)
    
    # Si no hay crímenes para el área, retornar
    if crímenes_area is None:
        return f"No se encontraron crímenes para el área: {area_name}"
    
    # Listar todos los crímenes en el área
    crímenes_filtrados = al.new_list()
    for fila in crímenes_area["elements"]:
        al.add_last(crímenes_filtrados, fila)
    
    # Ordenar los crímenes por fecha en orden descendente, si las fechas son iguales, ordenar por área
    crímenes_ordenados = al.merge_sort(crímenes_filtrados, compare_crit_by_date_desc)
    
    # Tomar los primeros N crímenes
    crímenes_n = crímenes_ordenados["elements"][:N]
    
    # Mostrar la cantidad total de crímenes y la información de los primeros N crímenes
    retorno += f"Total de crímenes reportados en el área {area_name}: {len(crímenes_area['elements'])}\n"
    
    for crimen in crímenes_n:
        fechaHora = str(crimen["DATE OCC"]).split(" ")
        retorno += (f"ID del crimen: {crimen['DR_NO']}\n"
                    f"Fecha del incidente: {fechaHora[0]}\n"
                    f"Hora del incidente: {fechaHora[1]}\n"
                    f"Área: {crimen['AREA NAME']}\n"
                    f"Subárea: {crimen['Rpt Dist No']}\n"
                    f"Parte del crimen: {crimen['Part 1-2']}\n"
                    f"Código del crimen: {crimen['Crm Cd']}\n"
                    f"Estado del caso: {crimen['Status Desc']}\n"
                    f"Dirección: {crimen['LOCATION']}\n"
                    f"\n===========================\n")
    
    return retorno

def compare_crit_by_date_desc(elm1, elm2):
    """
    Función para comparar dos crímenes. Compara por fecha (más reciente a más antiguo),
    si las fechas son iguales, compara por nombre del área (en orden descendente).
    """
    # Comparar por fecha (más reciente primero)
    if elm1["DATE OCC"] > elm2["DATE OCC"]:
        return True
    elif elm1["DATE OCC"] == elm2["DATE OCC"]:
        # Si las fechas son iguales, comparar por área (de mayor a menor)
        return elm1["AREA NAME"] > elm2["AREA NAME"]
    return False


def req_4(catalog,N,edad_in,edad_fin):
    """
    Retorna el resultado del requerimiento 4
    """
    
    filtro = rbt.values(catalog["Edad"]["data"],edad_in,edad_fin)
    leves = al.new_list()
    graves = al.new_list()
    for i in range(sl.size(filtro)):
        elm = sl.get_element(filtro,i)
        for fila in elm["elements"]:
            if int(fila["Part 1-2"]) == 1:
                al.add_last(graves,fila)
            else:
                al.add_last(leves,fila)

    ordenadosLeve = al.merge_sort(leves,sort_crit_by_age)
    ordenadosGrave = al.merge_sort(graves,sort_crit_by_age) 

    ordenadosLeve = ordenadosLeve["elements"][:N]   
    ordenadosGrave = ordenadosGrave["elements"][:N]




def sort_crit_by_age(elm1,elm2):
    isSorted = False

    fecha1 = elm1["Vict Age"]
    fecha2 = elm2["Vict Age"]
    area1 = elm2["DATE OCC"]
    area2 = elm2["DATE OCC"]
    
    if fecha1 > fecha2:
        isSorted = True
    elif fecha1 == fecha2:
        if area1 < area2:
            isSorted = True
    
    return isSorted

def req_5(catalog,n_areas,fecha_in,fecha_fin):
    #Definición de variables generales:
    fecha_in = fecha_a_Datetime(fecha_in)
    fecha_fin = fecha_a_Datetime(fecha_fin)
    rubro = catalog['Area']['data']
    llaves = mp.key_set(rubro)
    values = mp.value_set(rubro)
    for i in range(values['size']):
        filas = values['elements'][i]
        j = 0
        while j < filas['size']:
            fecha = filas['elements'][j]['DATE OCC']
            if fecha > fecha_fin or fecha < fecha_in:
                al.remove(filas,filas['elements'][j])
                j += 1
            j += 1
    
    return filas
    

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
