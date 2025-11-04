#Hola a todos :DD
import mysql.connector as dbc # requiere "pip install mysql-connector-python" en cmd
conection = dbc.connect(user='root', password='Omarfgc113.', #Para pruebas cada quien debe poner su contraseña de MySQL
                        host='127.0.0.1',
                        database="datos_tienda")

print("Se logro conectar a la DB, podemos seguir con el resto de actividades")