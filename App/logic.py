import time
import csv
from datetime import datetime as dt
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import single_linked_list as sl

csv.field_size_limit(2147483647)

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {}
    
    
    catalog['DR_NO'] = {'data': rbt.new_map(), 'size': 0}
    catalog['Date Rptd'] = {'data': rbt.new_map(), 'size': 0}
    catalog['DATE OCC'] = {'data': rbt.new_map(), 'size': 0}
    catalog['AREA NAME'] = {'data': rbt.new_map(), 'size': 0}
    catalog['Crm Cd'] = {'data': rbt.new_map(), 'size': 0}
    
    # Creamos una lista para almacenar los registros completos
    catalog['records'] = {'data': [], 'size': 0}
    
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    

# Funciones de consulta sobre el catálogo

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
    start_date = dt.strptime(start_date, "%Y-%m-%d")
    end_date = dt.strptime(end_date, "%Y-%m-%d")

  
    filtered_reports = []

    
    for crime_date in rbt.keys(catalog['dateIndex'], start_date.date(), end_date.date()):
      
        crime_list = rbt.get(catalog['dateIndex'], crime_date)
        
        
        for crime in crime_list:
            filtered_reports.append({
                'DR_NO': crime['DR_NO'],
                'Date Occurred': crime['DATE OCC'],
                'Time Occurred': crime['TIME OCC'],
                'Area Name': crime['AREA NAME'],
                'Crime Code': crime['Crm Cd'],
                'Location': crime['LOCATION'],
                'Crime Date': crime_date  
            })
    
    
    sorted_reports = sort_reports(filtered_reports)

    return sorted_reports

#ACA HACEMOS UNA FUNCION SECUNDARIA PARA EL REQUERIMIENTO 1

def sort_reports(filtered_reports):
    """
    Ordena los reportes primero por fecha (más reciente a más antiguo) y luego por área si es necesario.
    """
    sorted_reports = []
    
    while filtered_reports:
        most_recent = filtered_reports[0]
        
     
        for report in filtered_reports:
            if report['Crime Date'] > most_recent['Crime Date'] or (report['Crime Date'] == most_recent['Crime Date'] and report['Area Name'] < most_recent['Area Name']):
                most_recent = report
        
        
        sorted_reports.append(most_recent)
        
        
        filtered_reports = [report for report in filtered_reports if report != most_recent]
    
    return sorted_reports

def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    start_date = dt.strptime(start_date, "%Y-%m-%d")
    end_date = dt.strptime(end_date, "%Y-%m-%d")
    
    


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


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

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
