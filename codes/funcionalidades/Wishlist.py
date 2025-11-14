import sqlite3

class WishlistManager:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
    
    def agregar_producto(self, usuario_id, producto_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO wishlist (user_id, product_id) VALUES (?, ?)", 
                         (usuario_id, producto_id))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
    
    def obtener_wishlist(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT p.product_id, p.nombre, p.precio, p.imagen_url
                FROM wishlist w 
                JOIN products p ON w.product_id = p.product_id
                WHERE w.user_id = ?
            ''', (usuario_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Error:", e)
            return []
    
    def eliminar_producto(self, usuario_id, producto_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM wishlist WHERE user_id=? AND product_id=?", 
                         (usuario_id, producto_id))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False