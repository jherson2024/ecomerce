from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.imports import *
from models import Usuario
from utils.auth import hash_password, verify_password, create_access_token
from utils.keygen import generate_uint64_key
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# --- Modelos ---
class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    clave: str
    telefono: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    clave: str


# ===============================
# 🔵 Registro de usuario
# ===============================
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    # ¿Correo ya registrado?
    existe = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existe:
        raise HTTPException(400, detail="El correo ya está registrado.")

    nuevo = Usuario(
        id=int(generate_uint64_key()),   # 🔥 GENERACIÓN DE ID 100% SEGURO
        nombre=user.nombre,
        email=user.email,
        clave=hash_password(user.clave),
        telefono=user.telefono,
        estado="A",
        rol_id=2  # Cliente por defecto
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "message": "Usuario registrado correctamente",
        "usuario": {
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "email": nuevo.email
        }
    }


# ===============================
# 🟣 Login de usuario
# ===============================
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(Usuario).filter(Usuario.email == data.email).first()

    if not user:
        raise HTTPException(400, detail="Correo o contraseña incorrectos.")

    if not verify_password(data.clave, user.clave):
        raise HTTPException(400, detail="Correo o contraseña incorrectos.")

    token = create_access_token({"sub": str(user.id)})

    return {
        "message": "Login exitoso",
        "token": token,
        "usuario": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email
        }
    }
