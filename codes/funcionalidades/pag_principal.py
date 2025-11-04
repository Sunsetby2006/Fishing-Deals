from fastapi import FastAPI, HTTPException
from conection import get_connection
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para obtener el detalle de un producto específico
@app.get("/api/product/{product_id}", response_model=Dict[str, Any])
def get_product_details(product_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        print(f"Buscando producto con ID: {product_id}")
        
        # 1. Obtener los detalles principales del producto
        product_query = """
        SELECT product_id, nombre, descripcion, precio, stock, image_url
        FROM products 
        WHERE product_id = %s
        """
        cursor.execute(product_query, (product_id,))
        product_data = cursor.fetchone()

        print(f"Resultado de producto: {product_data}")

        if not product_data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # 2. Obtener las reseñas y calcular el promedio
        reviews_query = """
        SELECT r.score, r.coment, u.nombre as user_name, r.fecha
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.product_id = %s
        ORDER BY r.fecha DESC
        """
        cursor.execute(reviews_query, (product_id,))
        reviews_list = cursor.fetchall()
        
        print(f"Resultado de reseñas: {reviews_list}")

        # Cálculo de promedio y total de opiniones
        total_reviews = len(reviews_list)
        average_score = 0.0
        if total_reviews > 0:
            total_score = sum(review['score'] for review in reviews_list)
            average_score = round(total_score / total_reviews, 1)

        # 3. Datos de ejemplo para las variantes - CORREGIDO
        # Convertir el precio decimal a float antes de multiplicar
        #precio_base = float(product_data['precio'])
        #variants = [
        #    {"etiqueta": "4 Piezas", "precio": precio_base},
        #    {"etiqueta": "6 Piezas", "precio": precio_base * 1.5},
        #    {"etiqueta": "8 Piezas", "precio": precio_base * 2},
        #]
        
        # 4. Construir la respuesta final
        response_data = {
            "product": product_data,
            "reviews": reviews_list,
            "average_score": average_score,
            "total_reviews": total_reviews,
        #    "variants": variants
        }
        
        print(f"Respuesta final: {response_data}")
        return response_data
        
    except Exception as e:
        print(f"Error en la consulta: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint para verificar la base de datos
@app.get("/api/test-db")
def test_database():
    conn = get_connection()
    if conn is None:
        return {"status": "error", "message": "No se pudo conectar a la base de datos"}
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si existe la tabla products
        cursor.execute("SHOW TABLES LIKE 'products'")
        products_table = cursor.fetchone()
        
        # Verificar si existe la tabla users
        cursor.execute("SHOW TABLES LIKE 'users'")
        users_table = cursor.fetchone()
        
        # Verificar si existe la tabla reviews
        cursor.execute("SHOW TABLES LIKE 'reviews'")
        reviews_table = cursor.fetchone()
        
        # Contar productos
        cursor.execute("SELECT COUNT(*) as count FROM products")
        products_count = cursor.fetchone()
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()
        
        return {
            "status": "success",
            "tables": {
                "products": bool(products_table),
                "users": bool(users_table),
                "reviews": bool(reviews_table)
            },
            "counts": {
                "products": products_count['count'],
                "users": users_count['count']
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint de prueba para verificar que el servidor funciona
@app.get("/")
def read_root():
    return {"message": "Servidor FastAPI funcionando correctamente"}

# Endpoint para obtener todos los productos
@app.get("/api/products")
def get_all_products():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT product_id, nombre, precio, image_url 
        FROM products 
        LIMIT 24
        """
        cursor.execute(query)
        products = cursor.fetchall()
        
        return {"products": products}
        
    except Exception as e:
        print(f"Error en la consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        if conn:
            cursor.close()
            conn.close()