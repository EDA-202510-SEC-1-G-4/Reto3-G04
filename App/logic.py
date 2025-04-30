import time
import csv
import math
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
    
   
    filas = catalog['filas']['elements']
    
    
    crímenes_filtrados = al.new_list()
    
   
    for fila in filas:
        
        crime_date = fila["DATE OCC"]
        
       
        if start_date <= crime_date <= end_date:
            al.add_last(crímenes_filtrados,fila)
    
    
    al.merge_sort(crímenes_filtrados, compare_crit_by_date)

    
    for fila in crímenes_filtrados["elements"]:
        fechaHora = str(fila["DATE OCC"]).split(" ")
        retorno += (f"ID del crimen: {fila['DR_NO']}\n"
                    f"Fecha del incidente: {fechaHora[0]}\n"
                    f"Hora del incidente: {fechaHora[1]}\n"
                    f"Área: {fila['AREA NAME']}\n"
                    f"Subárea: {fila['Rpt Dist No']}\n"
                    f"Parte del crimen: {fila['Part 1-2']}\n"
                    f"Código del crimen: {fila['Crm Cd']}\n"
                    f"Estado del caso: {fila['Status Desc']}\n"
                    f"Dirección: {fila['LOCATION']}\n"
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


def req_3(catalog, N , area_name):
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
    retornoGraves = ""
    retornoLeves = ""
    edad_fin = str(edad_fin)
    edad_in = str(edad_in)
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

    for elm in ordenadosGrave:
        fechaHora = str(elm["DATE OCC"]).split(" ")
        retornoGraves += (f"Identificador: {elm['DR_NO']}\n"
                  f"Fecha del incidente: {fechaHora[0]}\n"
                  f"Hora del incidente: {fechaHora[1]}\n"
                  f"Área: {elm['AREA NAME']}\n"
                  f"Subárea: {elm['Rpt Dist No']}\n"
                  f"Gravedad del crimen: Grave (1)\n"
                  f"Código del crimen: {elm['Crm Cd']}\n"
                  f"Edad de la víctima: {elm['Vict Age']}\n"
                  f"Estado del caso: {elm['Status Desc']}\n"
                  f"Dirección del crimen: {elm['LOCATION']}\n"
                  f"\n===========================\n")
        
    for elm in ordenadosLeve:
                fechaHora = str(elm["DATE OCC"]).split(" ")
                retornoLeves += (f"Identificador: {elm['DR_NO']}\n"
                          f"Fecha del incidente: {fechaHora[0]}\n"
                          f"Hora del incidente: {fechaHora[1]}\n"
                          f"Área: {elm['AREA NAME']}\n"
                          f"Subárea: {elm['Rpt Dist No']}\n"
                          f"Gravedad del crimen: Leve (2)\n"
                          f"Código del crimen: {elm['Crm Cd']}\n"
                          f"Edad de la víctima: {elm['Vict Age']}\n"
                          f"Estado del caso: {elm['Status Desc']}\n"
                          f"Dirección del crimen: {elm['LOCATION']}\n"
                          f"\n===========================\n")
    return retornoGraves, retornoLeves




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
        if area1 > area2:
            isSorted = True
    
    return isSorted

def req_5(catalog,n_areas,fecha_in,fecha_fin):
    #Definición de variables generales:
    fecha_in = fecha_a_Datetime(fecha_in)
    fecha_fin = fecha_a_Datetime(fecha_fin)
    rubro = catalog['Area']['data']
    keys = mp.key_set(rubro)
    values = mp.value_set(rubro)
    no_resueltos = 0
    date_min = dt.strptime("12/31/2100", "%m/%d/%Y")
    date_max = dt.strptime("01/01/0001", "%m/%d/%Y")

    #variables auxiliares:
    areas_filtradas = al.new_list()
    
    #simplificar el hashmap en un diccionario:
    org = {}
    for i in range(keys['size']):
        org[keys['elements'][i]] = values['elements'][i]
    
    #filtro por fechas el diccionario:
    for i in range(keys['size']):
        filas = values['elements'][i]
        j = 0
        while j < org[keys['elements'][i]]['size']:
            fecha = filas['elements'][j]['DATE OCC']
            if fecha < fecha_in or fecha > fecha_fin:
                al.remove(org[keys['elements'][i]],org[keys['elements'][i]]['elements'][j])
                j -= 1
            else:
                if org[keys['elements'][i]]['elements'][j]['Status Desc'] == "Invest Cont":
                    no_resueltos += 1
                if org[keys['elements'][i]]['elements'][j]['DATE OCC'] < date_min:
                    date_min = org[keys['elements'][i]]['elements'][j]['DATE OCC']
                if org[keys['elements'][i]]['elements'][j]['DATE OCC'] > date_max:
                    date_max = org[keys['elements'][i]]['elements'][j]['DATE OCC']
            j += 1

    #unir area con size para ordenar: 
    ordenados = al.new_list()
    for area in org:
        al.add_last(ordenados,(area,org[area]['size']))
        al.add_last(areas_filtradas,area)
    ordenados = al.merge_sort(ordenados,cmp_function_req5)
    seleccionados = ordenados['elements'][0:n_areas]

    #Preparar retorno:
    retorno = {}
    for dupla in seleccionados:
        area_name,size = dupla
        if area_name in areas_filtradas['elements']:
            retorno[area_name] = org[area_name]

    date_min = dt.strftime(date_min, "%m/%d/%Y")[0:10]
    date_max = dt.strftime(date_max, "%m/%d/%Y")[0:10]

    return retorno, no_resueltos, date_min, date_max

def cmp_function_req5(elem1,elem2):
    area1, size1 = elem1
    area2, size2 = elem2
    res = False
    if size1 > size2:
        res = True
    return res

def req_6(catalog,n_areas,sex_vict,month):
    rubro = catalog['Area']['data']
    keys = mp.key_set(rubro)
    values = mp.value_set(rubro)

    #variable auxiliares:
    month_crimes = 0
    anual_crimes = {}
    areas_filtradas = al.new_list()

    org = {}
    for i in range(keys['size']):
        org[keys['elements'][i]] = values['elements'][i]
    
    #filtro por sexo y mes el diccionario:
    for i in range(keys['size']):
        filas = values['elements'][i]
        j = 0
        while j < org[keys['elements'][i]]['size']:
            sexo = filas['elements'][j]['Vict Sex']
            fecha = filas['elements'][j]['DATE OCC']
            mes = int(dt.strftime(fecha,"%m/%d/%Y")[0:2])
            anio = int(dt.strftime(fecha,"%m/%d/%Y")[6:10])
            if sexo != sex_vict and mes != month:
                al.remove(org[keys['elements'][i]],org[keys['elements'][i]]['elements'][j])
                j -= 1
            else:
                month_crimes += 1
                if anio not in anual_crimes:
                    anual_crimes[anio] = 1
                else:
                    anual_crimes[anio] += 1
            j += 1

    #unir area con size para ordenar: 
    ordenados = al.new_list()
    for area in org:
        al.add_last(ordenados,(area,org[area]['size']))
        al.add_last(areas_filtradas,area)
    ordenados = al.merge_sort(ordenados,cmp_function_req6)
    seleccionados = ordenados['elements'][0:n_areas]

    #Preparar anual crimes:
    a_crimes = al.new_list()
    for anio in anual_crimes:
        al.add_last(a_crimes,(anio,anual_crimes[anio]))
    
    #Preparar retorno:
    retorno = {}
    for dupla in seleccionados:
        area_name,size = dupla
        if area_name in areas_filtradas['elements']:
            retorno[area_name] = org[area_name]
    

    return retorno, month_crimes, a_crimes

def cmp_function_req6(elem1,elem2):
    area1, size1 = elem1
    area2, size2 = elem2
    res = False
    if size1 < size2:
        res = True
    return res


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass

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
    
    crímenes_area_interes = mp.get(catalog["Area"]["data"], area_name)
    
    if crímenes_area_interes is None:
        return f"No se encontraron crímenes para el área de interés: {area_name}"
    
    crímenes_area_filtrados = al.new_list()
    for crimen in crímenes_area_interes["elements"]:
        if crimen["Crm Cd"] == crm_cd:
            al.add_last(crímenes_area_filtrados,crimen)
            
    
    parejas_crímenes = al.new_list()

    for crimen_area_interes in crímenes_area_filtrados:
        fecha_crimen_area = crimen_area_interes["DATE OCC"]
        lat1, lon1 = float(crimen_area_interes["LAT"]), float(crimen_area_interes["LON"])
        
        # Ahora las coordenadas lat1, lon1 no son convertidas a int, sino que permanecen como floats.
        
        for area, crímenes_otros in catalog["Area"]["data"]["table"]["elements"]:
            if area != area_name:
                for crimen_otro in crímenes_otros["value"]:
                    if crimen_otro["Crm Cd"] == crm_cd:
                        fecha_crimen_otro = crimen_otro["DATE OCC"]
                        lat2, lon2 = float(crimen_otro["LAT"]), float(crimen_otro["LON"])
                        
                        # Calculamos la distancia entre los crímenes usando la fórmula de Haversine
                        distancia = haversine(lat1, lon1, lat2, lon2)
                        
                        
                        if fecha_crimen_area < fecha_crimen_otro:
                            pareja = (crimen_area_interes, crimen_otro, distancia)
                        else:
                            pareja = (crimen_otro, crimen_area_interes, distancia)
                        
                        al.add_last(parejas_crímenes,pareja)
    
    
    parejas_crímenes = sorted(parejas_crímenes, key=compare_crit_by_distance)

   
    parejas_más_cercanas = parejas_crímenes[:N]
    parejas_más_lejanas = parejas_crímenes[-N:]
    
    retorno += f"\n\nN crímenes más cercanos y lejanos del área de interés: {area_name} (Tipo: {crm_cd})\n"
    
  
    retorno += "\n--- 3 CRÍMENES MÁS CERCANOS ---\n"
    for pareja in parejas_más_cercanas:
        crimen1, crimen2, distancia = pareja
        fechaHora1 = str(crimen1["DATE OCC"]).split(" ")
        fechaHora2 = str(crimen2["DATE OCC"]).split(" ")
        retorno += (f"| {crimen1['Crm Cd']} | {crimen2['AREA NAME']} | {fechaHora1[0]} | {fechaHora2[0]} | {distancia:.2f} km |\n")

  
    retorno += "\n--- 3 CRÍMENES MÁS LEJANOS ---\n"
    for pareja in parejas_más_lejanas:
        crimen1, crimen2, distancia = pareja
        fechaHora1 = str(crimen1["DATE OCC"]).split(" ")
        fechaHora2 = str(crimen2["DATE OCC"]).split(" ")
        retorno += (f"| {crimen1['Crm Cd']} | {crimen2['AREA NAME']} | {fechaHora1[0]} | {fechaHora2[0]} | {distancia:.2f} km |\n")
    
    return retorno

def compare_crit_by_distance(pair):
    """
    Función para comparar dos crímenes. Compara por distancia.
    """
    return pair[2]

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
