import pandas as pd 
import random
from datetime import date
from datetime import timedelta

# fijamos la semilla
random.seed(0)

def convertirPesosEnRepeticiones(ListaConPesos):
    lista_repetidos =[]
    for elemento in ListaConPesos:
        entidad= elemento[0]
        for repetir in range(elemento[1]):
            lista_repetidos.append(entidad)
    return lista_repetidos

def compras_realizadas(productos_diferentes_repetidos, cantidad_de_producto_repetidos, posicion_compra_producto, posicion_compra, unidades_compras):
    cantidad_de_productos_elegidos = random.choice(productos_diferentes_repetidos)
    productos_elegidos =[]

    for productos in range(cantidad_de_productos_elegidos):
        cantidad = random.choice(cantidad_de_producto_repetidos)
        producto = random.randint(0,2)
        
        if(producto not in productos_elegidos):
            productos_elegidos.append(producto)
            unidades_compras.loc[posicion_compra_producto]=[posicion_compra, producto, cantidad]
            posicion_compra_producto +=1

    return [posicion_compra_producto, posicion_compra, unidades_compras]



    
# los distintos dataframes que se van a rellenar
usuarios = pd.DataFrame(columns = ['id_usuario', 'registro', 'pais', 'comprador'])
compras = pd.DataFrame(columns = ['dia', 'id_usuario', 'id_compra'])
unidades_compras = pd.DataFrame(columns = ['id_compra', 'id_producto', 'cantidad'])
producto = pd.DataFrame([[0,'Producto1', 50], [1,'Producto2', 100], [2, 'Producto3', 125]], columns = ['id_producto', 'descipcion', 'precio'])

# definir variables, algunas de ellas con pesos
productos_diferentes_elegidos_con_peso = [[1,10], [2,4], [3,1]]
productos_diferentes_repetidos = convertirPesosEnRepeticiones(productos_diferentes_elegidos_con_peso)

cantidad_de_producto_con_peso = [[1,8], [2,5],[3,2],[4,1]]
cantidad_de_producto_repetidos = convertirPesosEnRepeticiones(cantidad_de_producto_con_peso)

mes_dia = [[9,30],[10,31],[11,30],[12,18]]
fecha_maxima = date(2021,12,18)

paises_con_peso = [['Austria', 1], ['Belgium', 1], ['Bulgaria',1], ['Croatia',1] , ['Cyprus',1], 
        ['Czech Republic',1], ['Denmark',1], ['Estonia',1], ['Finland',1], ['France',20], ['Germany',2], 
        ['Greece',1], ['Hungary',1], ['Italy',20], ['Latvia',1], ['Lithuania',1], ['Luxembourg',1], ['Malta',1], 
        ['Netherlands',1], ['Poland',1], ['Portugal',15], ['Romania',1], ['Slovakia',1], ['Slovenia',1], 
        ['Spain',60], ['Sweden',1], ['United Kingdom',15]]
paises_repetidos = convertirPesosEnRepeticiones(paises_con_peso)

compras_3_meses_con_peso = [[0,20],[1,10],[2,4],[3,3],[4,2],[5,1],[6,1]]
compras_3_meses_repetidos = convertirPesosEnRepeticiones(compras_3_meses_con_peso)

# contadores iniciales
nuevos_usuarios = 10
posicion = 0
posicion_compra = 0
posicion_compra_producto = 0


# Rellenar los dataframes
for mes_y_dia in mes_dia:
    mes = mes_y_dia[0]

    for dia in range(1, mes_y_dia[1]):
        # para que no sea completamente lineal el crecimiento de usuarios
        variabilidad = random.randint(1, 10)
        fecha = date( 2021, mes, dia )

        for num_usuarios in range(nuevos_usuarios-variabilidad):    
            pais = random.choice(paises_repetidos)
            comprador = random.randint(0,1)
            # añadir usuario
            usuarios.loc[posicion] = [posicion, fecha, pais, comprador]

            # si el usuario es comprador añadir las compras
            if(comprador):
                # mismo dia del registro 
                compras.loc[posicion_compra]=[fecha, posicion, posicion_compra]
                [posicion_compra_producto, posicion_compra, unidades_compras]=compras_realizadas(productos_diferentes_repetidos, cantidad_de_producto_repetidos, posicion_compra_producto, posicion_compra, unidades_compras)
                posicion_compra += 1

                # misma semana
                for mas_compras in range(random.randint(0,2)):
                    dias_de_diferencia = random.randint(1,7)
                    fecha_compra_semana = fecha + timedelta(days=dias_de_diferencia)

                    # la fecha no puede ser mayor que esta
                    if(fecha_compra_semana<fecha_maxima):
                        compras.loc[posicion_compra]=[fecha_compra_semana, posicion, posicion_compra]
                        [posicion_compra_producto, posicion_compra, unidades_compras]=compras_realizadas(productos_diferentes_repetidos, cantidad_de_producto_repetidos, posicion_compra_producto, posicion_compra, unidades_compras)
                        posicion_compra += 1

                # siguientes 3 meses
                for mas_compras in range(random.choice(compras_3_meses_repetidos)):
                    dias_de_diferencia = random.randint(7,90)
                    fecha_compra_3m = fecha + timedelta(days=dias_de_diferencia)

                    # la fecha no puede ser mayor que esta
                    if(fecha_compra_3m<fecha_maxima):
                        compras.loc[posicion_compra]=[fecha_compra_3m, posicion, posicion_compra]
                        [posicion_compra_producto, posicion_compra, unidades_compras]=compras_realizadas(productos_diferentes_repetidos, cantidad_de_producto_repetidos, posicion_compra_producto, posicion_compra, unidades_compras)
                        posicion_compra += 1

            posicion += 1
        # crecimiento por dia
        nuevos_usuarios += 3
    

# escribir los dataframes en csv
usuarios.to_csv('datos/usuarios.csv')
compras.to_csv('datos/compras.csv')
unidades_compras.to_csv('datos/unidades_compras.csv')
producto.to_csv('datos/producto.csv')







