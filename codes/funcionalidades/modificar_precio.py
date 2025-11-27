from conection import get_connection
from datetime import date

def modificar_precio(user_id):
    conexion = get_connection()
    if conexion is None:
        print("Error de conexión a la base de datos")
        return
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT product_id, nombre, precio 
            FROM products 
            WHERE user_id = %s
        """, (user_id,))
        productos = cursor.fetchall()

        if not productos:
            print("No tienes productos registrados.")
            return

        print("\nTus productos:")
        for p in productos:
            print(f"ID: {p['product_id']} | Nombre: {p['nombre']} | Precio actual: ${p['precio']}")

        product_id = int(input("\nIngresa el ID del producto a modificar: "))
        nuevo_precio = float(input("Ingresa el nuevo precio: "))

        update_query = """
        UPDATE products 
        SET precio = %s 
        WHERE product_id = %s AND user_id = %s
        """
        cursor.execute(update_query, (nuevo_precio, product_id, user_id))
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"Precio actualizado correctamente. Nuevo precio: ${nuevo_precio}")
        else:
            print("No se pudo actualizar el precio. Verifica el ID del producto.")

    except Exception as e:
        print(f"Error al modificar precio: {e}")
    
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    try:
        user_id = int(input("Ingresa tu ID de usuario: "))
        modificar_precio(user_id)
    except ValueError:
        print("Debes ingresar un número válido para el ID de usuario.")


