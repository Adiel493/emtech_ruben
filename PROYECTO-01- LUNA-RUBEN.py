'''
Creado por Rubén Adiel Luna Medina
Proyecto Lifestore
13/02/2022
'''

from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

credenciales_verificadas = False #verifica si las credenciales en el login son correctas
intentos_acceso = 3 #controla intentos al iniciar sesión
user = "emtech" #nombre de usuario del sistema
password = "hcetme" #contraseña del sistema

ventas_productos = [] #lista de ventas por producto
busquedas_productos = [] #lista de busquedas por producto
resenas_productos = [] #lista de reseñas por producto
ventas_mensuales = [] #lista de ventas e ingresos mensuales
ventas_ingresos_categorias = [] #lista de ventas e ingresos por categorias


print("Bienvenido al Sistema de Reportes de LifeStore")


#LOGIN____________________________________________
while not credenciales_verificadas:

  usuario = input("\nIngrese su nombre de usuario: ")
  contrasena = input("\nIngrese su contraseña: ")

  #verificación de credenciales
  if(usuario == user and contrasena == password):
    credenciales_verificadas = True
    print("Acceso concedido")
  else: #Si el usuario o contraseña no coincide, se resta un intento
    intentos_acceso -= 1
    if(usuario == user): #Mensaje si la contraseña es incorrecta
      print("Contraseña incorrecta, favor de intentar de nuevo")
    else: #Mensaje si el usuario es incorrecto
      print("Usuario no encontrado, favor de intentar de nuevo")
    print(f"\nCuenta con {intentos_acceso} intentos")
    if(intentos_acceso == 0): #control de número de intentos
      exit()


#VENTAS___________________________________________
for product in lifestore_products:
  total_ventas = 0 #contador de ventas por producto
  total_devoluciones = 0 #contador de devoluciones por producto
  total_ventas_exitosas = 0 #contador de ventas sin contar devoluciones
  for sale in lifestore_sales:
    if(sale[1]==product[0]): 
      total_ventas += 1
      if(sale[4]==1): 
        total_devoluciones += 1
  #[id_producto, nombre_producto, número_de_ventas, número_de_devoluciones, número_de_ventas_exitosas (sin devoluciones)]
  ventas_productos.append([product[0],product[1],total_ventas,total_devoluciones,total_ventas - total_devoluciones])
ventas_ordenadas = sorted(ventas_productos, key=lambda venta : venta[4]) #lista con ventas ordenadas de menor a mayor
total_ventas = sum([venta[4] for venta in ventas_productos]) #Suma de todas las ventas realizadas 

#Categorización de ventas por categoría
categorias_ventas = {} #diccionario de categorias de acuerdo a las ventas
for venta in ventas_ordenadas: 
  id = venta[0]
  product_category = lifestore_products[id-1][3] #Se obtine la categoría del producto actual
  if product_category not in categorias_ventas.keys(): 
    categorias_ventas[product_category] = []
  categorias_ventas[product_category].append(venta) 


#BÚSQUEDAS___________________________________________
for product in lifestore_products:
  total_busquedas = 0 #Contador de busquedas por producto
  for search in lifestore_searches:
    if(search[1]==product[0]):
      total_busquedas += 1
  #[id_producto, número_de_busquedas]
  busquedas_productos.append([product[0],total_busquedas]) 

busquedas_ordenadas = sorted(busquedas_productos, key=lambda busqueda : busqueda[1]) #Lista ordenada de busquedas

#Categorización de busquedas por categoría
categorias_busquedas = {}
for busqueda in busquedas_ordenadas:
  id = busqueda[0]
  product_category = lifestore_products[id-1][3]
  if product_category not in categorias_busquedas.keys():
    categorias_busquedas[product_category] = []
  categorias_busquedas[product_category].append(busqueda)


#RESEÑAS_________________________________________________
for product in lifestore_products:
  total_resena = 0 #Suma de reseñas
  contador_resena = 0 #Contador de reseñas
  for sale in lifestore_sales:
    if(sale[1]==product[0]):
      total_resena += sale[2]
      contador_resena += 1
  if(contador_resena > 0):
    #[id_producto, promedio_reseñas, cantidad_reseñas]
    resenas_productos.append([product[0],round(total_resena/contador_resena,1),contador_resena]) 

resenas_ordenadas = sorted(resenas_productos, reverse = True, key=lambda resena : (resena[1], resena[2])) #Lista de reseñas ordenada de acuerdo al promedio de reseñas y la cantidad de reseñas


#INGRESOS_Y_VENTAS_TOTALES________________________________
fechas = [[sale[1], sale[3]] for sale in lifestore_sales if sale[4] == 0] #Lista que contiene las fechas de todas las ventas
meses = {} #diccionario de meses

#Categorización de venta de producto por mes
for fecha in fechas:
  id = fecha[0]
  _,mes,_ = fecha[1].split("/") #Se obtine mes del formato de fecha
  if mes not in meses.keys():
    meses[mes] = []
  meses[mes].append(id)

for key in meses.keys():
  lista_mes = meses[key]
  suma_venta = 0 #Suma de los precios de las ventas
  for id_producto in lista_mes:
    precio = lifestore_products[id_producto-1][2] #Se obtiene precio de producto actual para sumar
    suma_venta += precio
  #[mes, ingreso_mensual, ventas_mensuales]
  ventas_mensuales.append([key,suma_venta,len(lista_mes)]) 
  ventas_mensuales_ordenadas = sorted(ventas_mensuales, key= lambda mes:mes[0]) #lista ordenada de acuerdo a los meses

total_ingresos = sum([producto[1] for producto in ventas_mensuales]) #suma para calcular total de ingresos


#Categorización de ventas e ingresos por categoría
categorias_ventas_diccionario = {} #Diccionario de categorios de acuerdo a la lista de ventas

for sale in lifestore_sales:
  if(sale[4] == 0):
    id = sale[1]
    product_category = lifestore_products[id-1][3]
    if product_category not in categorias_ventas_diccionario.keys():
      categorias_ventas_diccionario[product_category] = []
    categorias_ventas_diccionario[product_category].append(id)

for key in categorias_ventas_diccionario.keys():
  lista_categoria = categorias_ventas_diccionario[key]
  suma_venta_categoria = 0
  for id_producto in lista_categoria:
    precio = lifestore_products[id_producto-1][2]
    suma_venta_categoria += precio
  #[categoria, ingresos_por_categoria, ventas_por_categoria]
  ventas_ingresos_categorias.append([key, suma_venta_categoria, len(lista_categoria)])




#REPORTE____________________________________________
print("\nLOS 5 PRODUCTOS MÁS VENDIDOS")
for venta in ventas_ordenadas[-5:]:
  print(f"Ventas: {venta[4]} Stock: {lifestore_products[venta[0]-1][4]} Producto: {venta[1]}")

print("\nLOS 5 PRODUCTOS MENOS VENDIDOS POR CATEGORÍA")
for key in categorias_ventas.keys():
  lista_categoria = categorias_ventas[key]
  print(f"\n{key.upper()}")
  for id_producto in lista_categoria[:5]:
    product_name = lifestore_products[id_producto[0]-1][1]
    product_stock = lifestore_products[id_producto[0]-1][4]
    print(f"   Ventas: {id_producto[4]} Stock: {product_stock} Producto: {product_name}")

print("\nLOS 10 PRODUCTOS CON MÁS BUSQUEDAS")
for busqueda in busquedas_ordenadas[-10:]:
  print(f"Busquedas: {busqueda[1]} Producto: {lifestore_products[busqueda[0]-1][1]}")

print("\nLOS 10 PRODUCTOS CON MENOS BUSQUEDAS POR CATEGORÍA")
for key in categorias_busquedas.keys():
  lista_categoria = categorias_busquedas[key]
  print(f"\n{key.upper()}") #Se imprime categoria en mayúscula 
  for id_producto in lista_categoria[:10]:
    product_name = lifestore_products[id_producto[0]-1][1]
    print(f"   Busquedas: {id_producto[1]} Producto: {product_name}")

print("\nLOS 5 PRODUCTOS CON MEJORES RESEÑAS")
for resena in resenas_ordenadas[:5]:
  print(f"Reseña: {resena[1]} Producto: {lifestore_products[resena[0]-1][1]}")

print("\nLOS 5 PRODUCTOS CON PEORES RESEÑAS")
for resena in resenas_ordenadas[-5:]:
  print(f"Reseña: {resena[1]} Producto: {lifestore_products[resena[0]-1][1]}")

print("\nVENTAS E INGRESOS POR MES")
for info_mensual in ventas_mensuales_ordenadas:
  #Cambio de formato de mes de númerico a categorico 
  if(info_mensual[0]=="01"):  
    mes = "Enero"
  elif(info_mensual[0]=="02"):
    mes = "Febrero"
  elif(info_mensual[0]=="03"):
    mes = "Marzo"
  elif(info_mensual[0]=="04"):
    mes = "Abril"
  elif(info_mensual[0]=="05"):
    mes = "Mayo"
  elif(info_mensual[0]=="06"):
    mes = "Junio"
  elif(info_mensual[0]=="07"):
    mes = "Julio"
  elif(info_mensual[0]=="08"):
    mes = "Agosto"
  elif(info_mensual[0]=="09"):
    mes = "Septiembre"
  elif(info_mensual[0]=="10"):
    mes = "Octubre"
  elif(info_mensual[0]=="11"):
    mes = "Noviembre"
  else:
    mes = "Diciembre"
  
  print(f"Mes: {mes} Ventas: {info_mensual[2]} Ingresos: ${info_mensual[1]}")

print("\nVENTAS E INGRESOS POR CATEGORÍA")
for categoria in ventas_ingresos_categorias:
  print(f"Categoría: {categoria[0]} Ventas: {categoria[2]} Ingresos: ${categoria[1]}")

print(f"\nLAS VENTAS TOTALES SON: {total_ventas} Y LOS INGRESOS TOTALES SON: ${total_ingresos}")


