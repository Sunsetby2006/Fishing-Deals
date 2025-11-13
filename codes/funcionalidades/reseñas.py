from conection import get_connection
from datetime import date

def calificar_producto():
    conexion = get_connection()
    cursor = conexion.cursor()
    product_id = int(input("Ingrese el ID del producto a reseñar:"))
    try:
        print(f"\nAgregar reseña para producto ID: {product_id}")
        user_id = int(input("Ingrese su ID de usuario: "))
        score = int(input("Ingrese calificacion (1-5): "))
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
if __name__ == "_main_":
    calificar_producto()