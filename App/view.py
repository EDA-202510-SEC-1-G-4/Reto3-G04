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
    retorno = log.load_data(control, filename)
    print(retorno)

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
    start_date = input("Ingrese la fecha de inicio (formato YYYY-MM-DD): ")
    end_date = input("Ingrese la fecha de fin (formato YYYY-MM-DD): ")


    start_time = log.get_time()
    result = log.req_1(control, start_date, end_date)
    total_records = len(result)

    
    if not result:
        print(f"No se encontraron crímenes entre las fechas {start_date} y {end_date}.")
    else:
        print(f"El número total de crímenes ocurridos entre {start_date} y {end_date} es: {total_records}")
        
        print("\nLos primeros 5 crímenes:")
        for i, crime in enumerate(result[:5]):
            print(f"{i+1}. {crime['DR_NO']} | {crime['Date Occurred']} | {crime['Time Occurred']} | {crime['Area Name']} | {crime['Crime Code']} | {crime['Location']}")
        
        print("\nLos últimos 5 crímenes:")
        for i, crime in enumerate(result[-5:]):
            print(f"{i+1}. {crime['DR_NO']} | {crime['Date Occurred']} | {crime['Time Occurred']} | {crime['Area Name']} | {crime['Crime Code']} | {crime['Location']}")

  
    end_time = log.get_time()
    execution_time = log.delta_time(start_time, end_time)
    print(f"\nEl tiempo tomado fue de {execution_time} ms")
    print("\n========================\n")

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


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
    # TODO: Imprimir el resultado del requerimiento 8
    pass


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
