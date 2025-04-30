import sys
import App.logic as log

default_limit = 1000

sys.setrecursionlimit(default_limit*10)

def new_logic():
    """
        Se crea una instancia del controlador
    """
    return log.new_logic()

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos
    """
    filename = "/Crime_in_LA_20.csv"
    start = log.get_time()

    retorno = log.load_data(control, filename)
    end = log.get_time()
    print(retorno)
    tiempo = log.delta_time(start,end)
    print(f"El timepo tomado fue de: {tiempo}")

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    start_date = input("Ingrese la fecha de inicio del reporte (formato MM/DD/YYYY): ")
    end_date = input("Ingrese la fecha de fin (formato MM/DD/YYYY): ")

    # Llamar a la función de lógica para obtener los crímenes dentro del rango de fechas
    start = log.get_time()
    resultado = log.req_1(control, start_date, end_date)
    print(resultado)
    end = log.get_time()

    # Imprimir el tiempo de ejecución
    tiempo = log.delta_time(start, end)
    print(f"El tiempo tomado fue de {tiempo} ms\n")

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    start_date = input("Ingrese la fecha de inicio del reporte (Date Rprtd) (formato MM/DD/YYYY): ")
    end_date = input("Ingrese la fecha de fin (formato MM/DD/YYYY): ")
    print()


    start = log.get_time()
    resultado = log.req_2(control, start_date, end_date)
    print(resultado)
    end = log.get_time()
    tiempo = log.delta_time(start,end)
    print(f"El tiempo tomado fue de {tiempo}\n")


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    area_name = input("Ingrese el nombre del área: ")
    N = int(input("Ingrese el número de crímenes a consultar: "))

    start = log.get_time()
    resultado = log.req_3(control, N, area_name)
    print(resultado)
    end = log.get_time()
    tiempo = log.delta_time(start,end)
    print(f"El tiempo tomado fue de {tiempo}\n")


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    N = int(input("Ingrese el número de crímenes a consultar: "))
    start_age = int(input("Ingrese la edad inicial: "))
    end_age = int(input("Ingrese la edad final: "))
    start = log.get_time()
    resultadoGraves, resultadoLeves = log.req_4(control, N, start_age, end_age)
    print("Resultado de crímenes graves:\n", resultadoGraves)
    print("Resultado de crímenes leves:\n", resultadoLeves)
    end = log.get_time()
    tiempo = log.delta_time(start, end)
    print(f"El tiempo tomado fue de {tiempo}\n")


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass
    n_areas = int(input('Numero de areas a consultar: '))
    fecha_in = str(input('Fecha inicial de busqueda (MM/DD/YYYY): '))
    fecha_fin = str(input('Fecha final de busqueda (MM/DD/YYYY): '))
    data, no_resueltos, date_min, date_max = log.req_5(control,n_areas,fecha_in,fecha_fin)
    retorno = ''
    for area in data:
        retorno += (f"\nArea donde ocurrio el crimen: {data[area]['elements'][0]['AREA']}\n"
                   f"Nombre del area donde ocurrio el crimen: {area}\n"
                   "==============================================\n")
                   
    retorno += (f"Crimenes no resueltos en el rango de fechas: {no_resueltos}\n"
                f"Fecha del primer crimen: {date_min}\n"
                f"Fecha del ultimo crimen: {date_max}\n"
                "==============================================\n")
    print(retorno)     


def print_req_6(control):
    n_areas = int(input("Numero de areas a consultar: "))
    sex_vict = str(input("Sexo de las victimas: "))
    month = int(input("Mes en el que ocurrieron los crimenes (MM): "))
    data = log.req_6(control,n_areas,sex_vict,month)
    print(data)

def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    area_name = input("Ingrese el nombre del área de interés: ")

    # Solicitar el número de crímenes a mostrar
    N = int(input("Ingrese el número N de crímenes a mostrar: "))

    # Solicitar el código del crimen
    crm_cd = input("Ingrese el código del tipo de crimen (crm_cd): ")

    # Llamar a la función de lógica para obtener los resultados
    start = log.get_time()
    resultado = log.req_8(control, N, area_name, crm_cd)
    end = log.get_time()

    # Imprimir los resultados
    print(resultado)

    # Medir el tiempo de ejecución
    tiempo = log.delta_time(start, end)
    print(f"\nTiempo de ejecución: {tiempo:.2f} ms")


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
