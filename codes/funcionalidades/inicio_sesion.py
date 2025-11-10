from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Enum, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import inspect
import os

app = FastAPI()

# Configuración de templates
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, "..", "diseños web")
template = Jinja2Templates(directory=template_dir)

# CONFIGURACIÓN MYSQL
DATABASE_URL = "mysql+pymysql://root:Tenorio18@localhost/datos_tienda"

print("Configurando conexión a MySQL...")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
def root(request: Request):
    return template.TemplateResponse("inicio.html", {"request": request})

@app.get("/signup")
def signup_form(request: Request):
    return template.TemplateResponse("registro.html", {"request": request})

@app.post("/signup")
def signup(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    contrasena: str = Form(...),
    direccion: str = Form(...),
    rol: str = Form("Cliente"),
    db: Session = Depends(get_db)
):
    try:
        print(f"Registrando usuario: {email}")
        
        # Verificar si el usuario ya existe usando SQL directo
        existing = db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email}).fetchone()
        if existing:
            return template.TemplateResponse("registro.html", {
                "request": request,
                "error": "El usuario ya existe"
            })
        
        # Insertar usando SQL directo
        db.execute(text("""
            INSERT INTO users (nombre, email, contrasena, direccion, rol) 
            VALUES (:nombre, :email, :contrasena, :direccion, :rol)
        """), {
            "nombre": nombre,
            "email": email,
            "contrasena": contrasena,
            "direccion": direccion,
            "rol": rol
        })
        db.commit()
        
        print(f"Usuario registrado: {email}")
        
        # Después del registro, redirigir al index.html
        return template.TemplateResponse("index.html", {
            "request": request,
            "usuario": {"nombre": nombre, "email": email, "rol": rol}
        })
    
    except Exception as e:
        db.rollback()
        print(f"Error en registro: {e}")
        return template.TemplateResponse("registro.html", {
            "request": request,
            "error": f"Error al crear usuario: {str(e)}"
        })

@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        print(f"Login intentado: {email}")
        
        # Buscar usuario usando SQL directo
        usuario = db.execute(
            text("SELECT * FROM users WHERE email = :email AND contrasena = :contrasena"),
            {"email": email, "contrasena": contrasena}
        ).fetchone()
        
        if not usuario:
            return template.TemplateResponse("inicio.html", {
                "request": request,
                "error": "Email o contraseña incorrectos"
            })
        
        # Convertir resultado a diccionario
        usuario_dict = dict(usuario._mapping)
        
        print(f"Login exitoso: {usuario_dict['nombre']} - Redirigiendo a index.html")
        
        # Redirigir al index.html después del login exitoso
        return template.TemplateResponse("index.html", {
            "request": request,
            "usuario": {
                "nombre": usuario_dict['nombre'],
                "email": usuario_dict['email'],
                "rol": usuario_dict['rol'],
                "direccion": usuario_dict['direccion']
            }
        })
    
    except Exception as e:
        print(f"Error en login: {e}")
        return template.TemplateResponse("inicio.html", {
            "request": request,
            "error": f"Error en el sistema: {str(e)}"
        })

@app.get("/user")
def user(request: Request):
    return template.TemplateResponse("user.html", {"request": request})

# Nueva ruta para la página principal (index.html)
@app.get("/home")
def home(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

# Endpoint de debug
@app.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    try:
        usuarios = db.execute(text("SELECT * FROM users")).fetchall()
        return {
            "total_usuarios": len(usuarios),
            "usuarios": [dict(u._mapping) for u in usuarios]
        }
    except Exception as e:
        return {"error": str(e)}
