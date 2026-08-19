def TomaDeValores():
    print("Ingrese la cantidad de filas:")
    filas = int(input())
    print("Ingrese la cantidad de columnas:")
    columnas = int(input())

    return filas, columnas



def CrearMatriz(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            print(f"Ingrese el valor para la posición ({i}, {j}):")
            valor = int(input())
            fila.append(valor)
        matriz.append(fila)

    print("matriz creada:")
    for fila in matriz:
        print(fila)
    return matriz

filas, columnas = TomaDeValores()
matriz = CrearMatriz(filas, columnas)


    