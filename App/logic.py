import time
import csv
import datetime as dt
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import single_linked_list as sl
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
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
    for fila in filas:
        
        rbt.put(catalog["ID"]["data"],fila["DR_NO"],fila)
        catalog["ID"]["size"] += 1
        rbt.put(catalog["Date_Rptd"]["data"],fila["Date Rptd"],fila)
        catalog["Date_Rptd"]["size"] += 1
        rbt.put(catalog["Date_Occrd"]["data"],fila["DATE OCC"],fila)
        catalog["Date_Occrd"]["size"] += 1
        mp.put(catalog["Area"]["data"],fila["AREA NAME"],fila)
        catalog["Area"]["size"] += 1
        rbt.put(catalog["Edad"]["data"],fila["Vict Age"],fila)
        catalog["Edad"]["size"] += 1
        rbt.put(catalog["Codigos"]["data"],fila["Crm Cd"],fila)
        catalog["Codigos"]["size"] += 1

        al.add_last(catalog["filas"],fila)

    cinco = []
    for i in range(5):
        cinco.append(catalog["filas"]["elements"][i])
    for i in range(1,6):
        cinco.append(catalog["filas"]["elements"][-i])

    for fila2 in cinco:
        retorno += (f"{fila2['DR_NO']}\n"
                f"{fila2['Date Rptd']}\n"
                f"{fila2['DATE OCC']}\n"
                f"{fila2['AREA NAME']}\n"
                f"{fila2['Crm Cd']}\n"
                f"\n =========================== \n")
        

    return retorno





def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


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


def req_5(catalog,areas,fecha_in,fecha_fin):
    fecha_in = dt.strptime(fecha_in,"%Y-%m-%d")
    fecha_fin = dt.strptime(fecha_fin,"%Y-%m-%d")

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
