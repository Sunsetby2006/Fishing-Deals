import sqlite3

class CarritoManager:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
    
    def agregar_producto(self, usuario_id, producto_id, cantidad=1):
        try:
            cursor = self.conn.cursor()
            # Verificar si ya existe
            cursor.execute("SELECT * FROM cart WHERE user_id=? AND product_id=?", 
                        (usuario_id, producto_id))
            if cursor.fetchone():
                # Si ya existe, actualizar cantidad
                cursor.execute("UPDATE cart SET cantidad=cantidad+? WHERE user_id=? AND product_id=?", 
                            (cantidad, usuario_id, producto_id))
            else:
                # Si no existe, insertar nuevo
                cursor.execute("INSERT INTO cart (user_id, product_id, cantidad) VALUES (?, ?, ?)", 
                            (usuario_id, producto_id, cantidad))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
    
    def obtener_carrito(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT p.product_id, p.nombre, p.precio, p.imagen_url, c.cantidad
                FROM cart c 
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = ?
            ''', (usuario_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Error:", e)
            return []
    
    def eliminar_producto(self, usuario_id, producto_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM cart WHERE user_id=? AND product_id=?", 
                        (usuario_id, producto_id))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
        