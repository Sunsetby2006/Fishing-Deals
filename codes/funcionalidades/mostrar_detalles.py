from conection import get_connection

conexion = get_connection()

print ("Bienvenido")
usuario = input("Usuario: ")
contraseña = input("Contraseña: ")

if conexion:
    cursor = conexion.cursor(dictionary = True)
    consulta = "SELECT * FROM users WHERE nombre = %s"
    cursor.execute(consulta, (usuario,))
    resultado = cursor.fetchone()

    if resultado:
        if resultado['contrasena'] == contraseña:
            print("Usuario autenticado")
            print(f"Nombre: {resultado['nombre']}")
            print(f"Correo: {resultado['email']}")
            print(f"Dirección: {resultado['direccion']}")
            print(f"Rol: {resultado['rol']}")
        else:
            print("Usuario o contraseña incorrecta.")
    else:
        print("Usuario o contraseña incorrecta.")
else:
    print("No se pudo conectar a la base de datos")
