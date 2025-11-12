from conection import get_connection
import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt

def get_user_info(user_id):
    """Función auxiliar temporal para simular el endpoint de FastAPI"""
    conn = get_connection()
    if conn is None:
        print("Error de conexión a la base de datos")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, nombre, email, direccion, rol
            FROM users 
            WHERE user_id = %s
        """, (user_id,))
        user_data = cursor.fetchone()
        return user_data
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
    finally:
        cursor.close()
        conn.close()


def subir_item(user_id):
    """Función de subida de productos (solo categoría 'Nuevo')"""
    conn = get_connection()
    if conn is None:
        print("Error de conexión a la base de datos")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)

        # Buscar el ID de la categoría "Nuevo"
        cursor.execute("SELECT category_id FROM categories WHERE nombre = %s", ("Nuevo",))
        categoria = cursor.fetchone()
        if not categoria:
            print("La categoría 'Nuevo' no existe.")
            return
        
        category_id = categoria["category_id"]

        # --- Inputs del vendedor ---
        print("\nAñadir nuevo producto (categoría: Nuevo)")
        nombre = input("Nombre del producto: ")
        descripcion = input("Descripción: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        image_url = input("URL de la imagen: ")

        # Insertar nuevo producto
        insert_query = """
        INSERT INTO products (nombre, descripcion, precio, stock, user_id, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            nombre, descripcion, precio, stock, user_id, category_id, image_url
        ))
        conn.commit()

        product_id = cursor.lastrowid
        
        print("\nProducto registrado exitosamente.")
        print(f"ID del producto: {product_id}")

    except Exception as e:
        print(f"Error en registro: {e}")
    
    finally:
        cursor.close()
        conn.close()

def ver_estats(sells):
    conn= get_connection()
    if conn in None:
        print("No se puede conectar a la DB")
        return
    
    try:
        cursos=conn.cursor(dictionary=True)

        #agarrar la tabla ventas
        query= "SELECT * FROM sells"
        info_ventas=pd.read_sql_query(query,conn)

        ventas_totales=info_ventas['sell_id'].count()
        ingresos_totales=info_ventas['ganancia'].sum()

        print(f"Ventas totales: {ventas_totales}")
        print(f"Ingresos totales: ${ingresos_totales},.2f")
        
        colores=sbn.color_palette("crest",n_colors=len(info_ventas))
        plt.fugure(figsize=(10,6))
        sbn.histplot(
            data=info_ventas,
            x="ganancia",
            bins=15,
            color="skyeblue",
            edgecolor="black"
        )

        plt.title("Distribución de ganancias por ventas")
        plt.xlabel("Ganancia por venta")
        plt.ylabel("Frecuecia")

        #Guardar imagen
        arch_nom="ventas.png"
        plt.savefig(arch_nom,dpi=300,bbox_inches="tight")
        print(f"\nGrafico guardado como '{arch_nom}'")

        plt.show()

    except Exception as e:
        print(f"Error al consultar datos:{e}")

    finally:
        if conn:
            conn.close
