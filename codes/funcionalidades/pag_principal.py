from fastapi import FastAPI, HTTPException
from conection import get_connection
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

# Modelos para autenticación
class LoginRequest(BaseModel):
    usuario: str
    contraseña: str

class RegisterRequest(BaseModel):
    nombre: str
    email: str
    contraseña: str
    direccion: str = ""

# Endpoint para login
@app.post("/api/login")
def login(login_data: LoginRequest):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Buscar usuario por nombre (como en mostrar_detalles.py)
        consulta = "SELECT * FROM users WHERE nombre = %s"
        cursor.execute(consulta, (login_data.usuario,))
        resultado = cursor.fetchone()

        if resultado:
            # Verificar contraseña
            if resultado['contrasena'] == login_data.contraseña:
                # Eliminar contraseña del response
                user_info = {
                    "user_id": resultado['user_id'],
                    "nombre": resultado['nombre'],
                    "email": resultado['email'],
                    "direccion": resultado['direccion'],
                    "rol": resultado['rol']
                }
                return {
                    "success": True,
                    "message": "Usuario autenticado",
                    "user": user_info
                }
            else:
                return {
                    "success": False,
                    "message": "Contraseña incorrecta"
                }
        else:
            return {
                "success": False,
                "message": "Usuario no encontrado"
            }
            
    except Exception as e:
        print(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint para registro
@app.post("/api/register")
def register(register_data: RegisterRequest):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si el usuario ya existe
        check_query = "SELECT * FROM users WHERE nombre = %s OR email = %s"
        cursor.execute(check_query, (register_data.nombre, register_data.email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return {
                "success": False,
                "message": "El nombre de usuario o email ya existe"
            }
        
        # Insertar nuevo usuario
        insert_query = """
        INSERT INTO users (nombre, email, contrasena, direccion, rol)
        VALUES (%s, %s, %s, %s, 'cliente')
        """
        cursor.execute(insert_query, (
            register_data.nombre,
            register_data.email,
            register_data.contraseña,
            register_data.direccion
        ))
        conn.commit()
        
        # Obtener el ID del usuario recién creado
        user_id = cursor.lastrowid
        
        return {
            "success": True,
            "message": "Usuario registrado exitosamente",
            "user_id": user_id
        }
            
    except Exception as e:
        print(f"Error en registro: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint para obtener información del usuario
@app.get("/api/user/{user_id}")
def get_user_info(user_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        user_query = """
        SELECT user_id, nombre, email, direccion, rol
        FROM users 
        WHERE user_id = %s
        """
        cursor.execute(user_query, (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user_data
        
    except Exception as e:
        print(f"Error en la consulta de usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

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

        # 3. Construir la respuesta final
        response_data = {
            "product": product_data,
            "reviews": reviews_list,
            "average_score": average_score,
            "total_reviews": total_reviews,
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
    return {"message": "Servidor FastAPI funcionando correctamente OwO"}

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

# Endpoint de filtrado por precio
@app.get("/api/filtrado")
def filtrar_productos_por_precio(precio_min: float, precio_max: float):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        consulta = """
        SELECT product_id, nombre, descripcion, precio, image_url
        FROM products
        WHERE precio BETWEEN %s AND %s
        ORDER BY precio ASC
        """
        cursor.execute(consulta, (precio_min, precio_max))
        resultados = cursor.fetchall()
        
        return {
            "filtro": {
                "precio_min": precio_min,
                "precio_max": precio_max
            },
            "productos": resultados,
            "total_productos": len(resultados)
        }
        
    except Exception as e:
        print(f"Error en el filtrado: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint de busqueda
@app.get("/api/buscar")
def buscar_productos(query: str):
    """
    Busca productos en la base de datos cuyo nombre o descripción contenga el texto proporcionado.
    """
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT product_id, nombre, descripcion, precio, stock, image_url
            FROM products
            WHERE nombre LIKE %s OR descripcion LIKE %s
            LIMIT 20
        """
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query))
        resultados = cursor.fetchall()
        
        return {
            "query": query, 
            "resultados": resultados,
            "total_resultados": len(resultados)
        }
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        raise HTTPException(status_code=500, detail="Error en la búsqueda")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoints para el panel de vendedor

# Endpoint para subir producto
@app.post("/api/vendedor/subir-producto")
def subir_producto(product_data: dict):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Buscar categoría "Nuevo"
        cursor.execute("SELECT category_id FROM categories WHERE nombre = %s", ("Nuevo",))
        categoria = cursor.fetchone()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría 'Nuevo' no encontrada")
        
        category_id = categoria["category_id"]

        # Insertar producto
        insert_query = """
        INSERT INTO products (nombre, descripcion, precio, stock, user_id, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            product_data["nombre"],
            product_data["descripcion"], 
            product_data["precio"],
            product_data["stock"],
            product_data["user_id"],
            category_id,
            product_data["image_url"]
        ))
        conn.commit()

        product_id = cursor.lastrowid
        
        return {
            "success": True,
            "message": "Producto registrado exitosamente",
            "product_id": product_id
        }
            
    except Exception as e:
        print(f"Error al subir producto: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

#Endpoint para los tstats
@app.get("/api/vendedor/estadisticas")
def obtener_estadisticas(user_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Estadísticas desde purchase_info
        cursor.execute("""
            SELECT 
                COUNT(*) as total_ventas,
                COALESCE(SUM(pi.precio_unitario * pi.cantidad), 0) as ingresos_totales,
                AVG(pi.precio_unitario * pi.cantidad) as promedio_venta,
                MAX(pi.precio_unitario * pi.cantidad) as venta_maxima,
                MIN(pi.precio_unitario * pi.cantidad) as venta_minima
            FROM purchase_info pi
            JOIN products p ON pi.product_id = p.product_id
            WHERE p.user_id = %s
        """, (user_id,))
        
        stats = cursor.fetchone()
        
        # Productos más vendidos desde purchase_info
        cursor.execute("""
            SELECT 
                p.nombre as producto_nombre,
                SUM(pi.cantidad) as unidades_vendidas,
                SUM(pi.precio_unitario * pi.cantidad) as ganancia_total
            FROM purchase_info pi
            JOIN products p ON pi.product_id = p.product_id
            WHERE p.user_id = %s
            GROUP BY p.product_id, p.nombre
            ORDER BY ganancia_total DESC
            LIMIT 5
        """, (user_id,))
        
        top_productos = cursor.fetchall()
        
        return {
            "estadisticas": stats,
            "top_productos": top_productos
        }
            
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint para obtener historial de ventas
@app.get("/api/vendedor/ventas")
def obtener_ventas_vendedor(user_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Buscar en purchase_info donde el producto pertenezca al vendedor
        cursor.execute("""
            SELECT 
                pi.info_id as venta_id,
                p.nombre as producto_nombre,
                pi.cantidad,
                pi.precio_unitario,
                pi.precio_unitario * pi.cantidad as ganancia_total,
                u.nombre as comprador_nombre,
                pur.fecha as fecha_venta,
                pur.estado
            FROM purchase_info pi
            JOIN products p ON pi.product_id = p.product_id
            JOIN purchase pur ON pi.purchase_id = pur.purchase_id
            JOIN users u ON pur.user_id = u.user_id  -- El comprador
            WHERE p.user_id = %s  -- El vendedor es el dueño del producto
            ORDER BY pur.fecha DESC
            LIMIT 20
        """, (user_id,))
        
        ventas = cursor.fetchall()
        
        return {"ventas": ventas}
            
    except Exception as e:
        print(f"Error al obtener ventas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Endpoint para obtener productos del vendedor
@app.get("/api/vendedor/productos")
def obtener_productos_vendedor(user_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT product_id, nombre, descripcion, precio, stock, image_url
            FROM products 
            WHERE user_id = %s
            ORDER BY product_id DESC
        """, (user_id,))
        
        productos = cursor.fetchall()
        
        return {"productos": productos}
            
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()