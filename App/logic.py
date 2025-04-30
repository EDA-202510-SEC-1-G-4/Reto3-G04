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
    
    
    start_date = fecha_a_Datetime(start_date)
    end_date = fecha_a_Datetime(end_date)
    
    
    fechas_filtradas = rbt.values(catalog["Date_Occrd"]["data"], start_date, end_date)
    
    
    crímenes_filtrados = al.new_list()
    
    
    for i in range(sl.size(fechas_filtradas)):
        fila = sl.get_element(fechas_filtradas, i)
        
        for crimen in fila["elements"]:
            
            al.add_last(crímenes_filtrados, crimen)
    
    
    crímenes_ordenados = al.merge_sort(crímenes_filtrados, compare_crit_by_date)

    
    if al.size(crímenes_ordenados) > 10:
        crímenes_ordenados = crímenes_ordenados["elements"][:5] + crímenes_ordenados["elements"][-5:]
    
   
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
    
    crímenes_area = mp.get(catalog["Area"]["data"], area_name)
    
   
    if crímenes_area is None:
        return f"No se encontraron crímenes para el área: {area_name}"
    
    
    crímenes_filtrados = al.new_list()
    for fila in crímenes_area["elements"]:
        al.add_last(crímenes_filtrados, fila)
    
   
    crímenes_ordenados = al.merge_sort(crímenes_filtrados, compare_crit_by_date_desc)
    
    
    crímenes_n = crímenes_ordenados["elements"][:N]
    
    
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
    55
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


import math
def haversine(lat1, lon1, lat2, lon2):
    # Convertir de grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # Radio de la Tierra en kilómetros
    return R * c

def req_8(catalog, N, area_name, crm_cd):
    """
    Requerimiento 8: Determinar los N crímenes más cercanos y lejanos del mismo tipo en otras áreas
    a partir de un área de interés.
    """
    retorno = ''
    
    # Obtener crímenes del área de interés con el código de crimen especificado
    crímenes_area_interés = mp.get(catalog["Area"]["data"], area_name)
    
    # Verificar si el área de interés existe
    if crímenes_area_interés is None:
        return f"No se encontraron crímenes para el área: {area_name}"

    crímenes_comparar = al.new_list()

    # Filtrar crímenes por código de crimen y el área de interés (búsqueda parcial)
    
    for fila in crímenes_area_interés["elements"]:
        if crm_cd.lower() in fila["Crm Cd"].lower():  # Comparación parcial
            al.add_last(crímenes_comparar, fila)

    # Si no hay crímenes para comparar en el área de interés, informar al usuario
    if al.size(crímenes_comparar) == 0:
        return f"No se encontraron crímenes de tipo {crm_cd} en el área: {area_name}"

    # Listar crímenes de otras áreas con el mismo código de crimen (búsqueda parcial)
    crímenes_otros = []
    for area in catalog["Area"]["data"]["table"]["elements"]:
        if area["key"] != area_name:  # Excluir el área de interés
            # Verificar si 'area["value"]' es válido antes de acceder
            if area["value"] is not None:
                for fila in area["value"]["elements"]:
                    if crm_cd.lower() in fila["Crm Cd"].lower():  # Comparación parcial
                        crímenes_otros.append(fila)

    # Verificar si hay crímenes en otras áreas con el mismo código de crimen
    if len(crímenes_otros) == 0:
        return f"No se encontraron crímenes de tipo {crm_cd} en áreas distintas a {area_name}."

    # Crear una lista de pares (crimen área interés, crimen otra área)
    parejas = []
    for crimen_area_interes in crímenes_comparar["elements"]:
        for crimen_otro_area in crímenes_otros:
            # Calcular la distancia usando Haversine
            lat1, lon1 = float(crimen_area_interes["LAT"]), float(crimen_area_interes["LON"])
            lat2, lon2 = float(crimen_otro_area["LAT"]), float(crimen_otro_area["LON"])
            distancia = haversine(lat1, lon1, lat2, lon2)

            # Comparar las fechas y asegurarse de que el crimen más antiguo aparezca primero
            fecha_area_interes = str(crimen_area_interes["DATE OCC"]).split(" ")
            fecha_otro_area = str(crimen_otro_area["DATE OCC"]).split(" ")
            
            if fecha_area_interes[0] < fecha_otro_area[0] or (fecha_area_interes[0] == fecha_otro_area[0] and fecha_area_interes[1] < fecha_otro_area[1]):
                parejas.append([crimen_area_interes, crimen_otro_area, distancia])
            else:
                parejas.append([crimen_otro_area, crimen_area_interes, distancia])

    # Ordenar las parejas por distancia (implementación explícita de la comparación)
    for i in range(len(parejas)):
        for j in range(i + 1, len(parejas)):
            if parejas[i][2] > parejas[j][2]:
                parejas[i], parejas[j] = parejas[j], parejas[i]  # Intercambio manual

    # Seleccionar los N crímenes más cercanos y más lejanos
    parejas_cercanas = parejas[:N]
    parejas_lejanas = parejas[-N:]

    # Formatear la salida
    retorno += f"Total de comparaciones realizadas: {len(parejas)}\n"
    
    for pareja in parejas_cercanas:
        print(pareja)
        retorno += (f"Crimen del área de interés (más antiguo): {pareja[1]['DR_NO']} - {pareja[1]['DATE OCC']} | {pareja[1]['AREA NAME']}\n"
                    f"Crimen de otra área (más reciente): {pareja[0]['DR_NO']} - {pareja[0]['DATE OCC']} | {pareja[0]['AREA NAME']}\n"
                    f"Distancia entre los crímenes: {pareja[2]} km\n"
                    f"\n===========================\n")

    for pareja in parejas_lejanas:
        print(pareja)
        retorno += (f"Crimen del área de interés (más antiguo): {pareja[1]['DR_NO']} - {pareja[1]['DATE OCC']} | {pareja[1]['AREA NAME']}\n"
                    f"Crimen de otra área (más reciente): {pareja[0]['DR_NO']} - {pareja[0]['DATE OCC']} | {pareja[0]['AREA NAME']}\n"
                    f"Distancia entre los crímenes: {pareja[2]} km\n"
                    f"\n===========================\n")

    return retorno

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
