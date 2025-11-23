from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.imports import *
from models import *
import random

router = APIRouter(
    prefix="/tienda",
    tags=["Tienda"]
)


@router.get("/detalle/{vendedor_id}")
def detalle_tienda(
    vendedor_id: int,
    db: Session = Depends(get_db)
):
    vendedor = (
        db.query(Vendedor)
        .filter(Vendedor.id == vendedor_id, Vendedor.estado == "A")
        .first()
    )

    if not vendedor:
        raise HTTPException(status_code=404, detail="La tienda no existe o está inactiva")

    # --- Logo de la tienda ---
    logo = f"{URL_SERVER}{IMAGENES_TIENDA_LOGO_DIR}{vendedor.logo}" if vendedor.logo else None

    # --- Políticas ---
    politicas = vendedor.politicatienda[0] if vendedor.politicatienda else None
    politicas_info = {
        "envio": politicas.politicaenvio if politicas else None,
        "devolucion": politicas.politicadevolucion if politicas else None,
        "privacidad": politicas.politicaprivacidad if politicas else None,
        "ultima_actualizacion": politicas.fechaactualizacion.strftime("%Y-%m-%d") if politicas else None
    }

    # --- Productos ---
    productos = []
    for p in vendedor.producto:
        if p.estado == "A" and p.stock > 0:
            productos.append({
                "id": str(p.id),
                "nombre": p.nombre,
                "precio": float(p.precio),
                "imagen": f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}" if p.fotoprincipal else None
            })

    # --- Colecciones con imágenes collage ---
    colecciones = []
    for c in vendedor.colecciontienda:
        if c.estadoregistro != "A":
            continue

        # Obtener productos activos de esta colección
        productos_coleccion = [
            p for p in c.producto
            if p.estado == "A" and p.stock > 0 and p.fotoprincipal
        ]

        # Construir URLs completas
        imagenes = [
            f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}"
            for p in productos_coleccion
        ]

        # Elegir 4 imágenes max al azar
        imagenes_collage = random.sample(imagenes, min(len(imagenes), 4)) if imagenes else []

        colecciones.append({
            "id": str(c.id),
            "nombre": c.nombre,
            "descripcion": c.descripcion,
            "imagenes": imagenes_collage  # <-- NUEVO
        })

    # --- Ubicación ---
    ubicacion = f"{vendedor.distrito.nombre}, {vendedor.distrito.provincia.nombre}" if vendedor.distrito else None

    # --- Promedio general de reseñas ---
    todas_reseñas = [
        r.puntuacion
        for p in vendedor.producto
        for r in p.resena
        if r.estado == "A"
    ]

    promedio_resena = round(sum(todas_reseñas) / len(todas_reseñas), 1) if todas_reseñas else 0

    # --- Respuesta final ---
    return {
        "tienda": {
            "id": str(vendedor.id),
            "nombre": vendedor.nombretienda,
            "descripcion": vendedor.descripcion,
            "logo": logo,
            "ubicacion": ubicacion,
            "politicas": politicas_info,
            "promedio_resenas": promedio_resena,
            "total_productos": len(productos),
            "total_colecciones": len(colecciones)
        },
        "productos": productos,
        "colecciones": colecciones
    }
@router.get("/{vendedor_id}/coleccion/{coleccion_id}")
def detalle_coleccion(
    vendedor_id: int,
    coleccion_id: int,
    db: Session = Depends(get_db)
):
    coleccion = (
        db.query(Colecciontienda)
        .filter(
            Colecciontienda.id == coleccion_id,
            Colecciontienda.vendedor_id == vendedor_id,
            Colecciontienda.estadoregistro == "A"
        )
        .first()
    )

    if not coleccion:
        raise HTTPException(status_code=404, detail="Colección no encontrada")

    vendedor = coleccion.vendedor

    # --- Imagenes collage ---
    productos_activos = [
        p for p in coleccion.producto
        if p.estado == "A" and p.stock > 0 and p.fotoprincipal
    ]

    imagenes = [
        f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}"
        for p in productos_activos
    ]

    collage = random.sample(imagenes, min(len(imagenes), 4)) if imagenes else []

    # --- Productos ---
    productos = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}"
        }
        for p in productos_activos
    ]

    return {
        "coleccion": {
            "id": coleccion.id,
            "nombre": coleccion.nombre,
            "descripcion": coleccion.descripcion,
            "imagenes": collage
        },
        "tienda": {
            "id": vendedor.id,
            "nombre": vendedor.nombretienda,
            "logo": f"{URL_SERVER}{IMAGENES_TIENDA_LOGO_DIR}{vendedor.logo}" if vendedor.logo else None
        },
        "productos": productos
    }
