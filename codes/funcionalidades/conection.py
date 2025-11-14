#Hola a todos :DD
import mysql.connector
import mysql.connector as dbc # requiere "pip install mysql-connector-python" en cmd

def get_connection():
    try:
        connection = dbc.connect(
            user='root', password='Omarfgc113.',  # Para pruebas cada quien debe poner su contraseña de MySQL
            host='127.0.0.1', database="datos_tienda"
        )
        print("Se logró conectar a la DB, podemos seguir con el resto de actividades")
        return connection
    except Exception as e:
        print(f"Error al conectar a la DB: {e}")
        return None

print("probando conexion")
get_connection()

