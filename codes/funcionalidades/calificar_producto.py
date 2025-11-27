import mysql.connector
from datetime import date

SESSION_USER_ID = None  

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Gi1tco0m222307",
            database="datos_tienda"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

def calificar_producto():
    # Verificación de sesión
    if SESSION_USER_ID is None:
        print("Debes iniciar sesión para poder escribir una reseña.")
        print("Redirigiendo a pantalla de login/registro...")
        return

    conexion = get_connection()
    if conexion is None:
        return
    
    cursor = conexion.cursor()
    product_id = int(input("Ingrese el ID del producto a reseñar: "))
    try:
        print(f"\nAgregar reseña para producto ID: {product_id}")
        user_id = SESSION_USER_ID  
        score = int(input("Ingrese calificación (1-5): "))
        coment = input("Reseña (máx 300 caracteres): ")
        fecha = date.today()

        if score < 1 or score > 5:
            print("La calificación debe estar entre 1 y 5.")
            return

        cursor.execute("""
            SELECT * FROM reviews
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        existente = cursor.fetchone()

        if existente:
            print("Ya has dejado una reseña para este producto.")
        else:
            cursor.execute("""
                INSERT INTO reviews (user_id, product_id, score, coment, fecha)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, product_id, score, coment, fecha))
            conexion.commit()
            print("Reseña guardada exitosamente.")
    except Exception as e:
        print(f"Error al guardar reseña: {e}")
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    calificar_producto()

