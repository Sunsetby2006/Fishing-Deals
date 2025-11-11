import seaborn as sb
import matplotlib.pyplot as mpl
from conection import get_connection
import mysql.connector

def subir_item(x):
      conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Insertar nuevo item
        insert_query = """
        INSERT INTO products (nombre, descripcion, precio, stock, user_id, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, 'Nuevo', %s)
        """
        cursor.execute(insert_query, (
            register_data.nombre,
            register_data.descripcion,
            register_data.precio,
            register_data.stock,
            register_data.user_id,
            register_data.image_url
        ))
        conn.commit()
        
        # Obtener el ID del usuario recién creado
        user_id = cursor.lastrowid
        
        return {
            "success": True,
            "message": "Item registrado exitosamente",
            "user_id": user_id,
            "product_id": product_id,
        }
            
    except Exception as e:
        print(f"Error en registro: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()
