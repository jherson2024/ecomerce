from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from core.imports import get_db
from core.globals import URL_SERVER, IMAGENES_PRODUCTO_DIR

from models import (
    Pedido, Pedidodetalle, Producto, Estadogeneral
)

router = APIRouter(
    prefix="/pedido",
    tags=["Pedidos"]
)

# ----------------------------------------------------------------------
# 🔥 UTILIDADES DE SERIALIZACIÓN
# ----------------------------------------------------------------------

def serialize_pedido(p: Pedido):
    return {
        "id": str(p.id),
        "usuario_id": p.usuario_id,
        "total": float(p.total),
        "fecha": p.fecha,
        "estado": p.estadogeneral.nombre if p.estadogeneral else None,
        "direccionentrega": p.direccionentrega,
        "referencia": p.referencia,
        "distrito_id": p.distrito_id,
        "metodopago_id": p.metodopago_id,
        "vendedor_id": p.vendedor_id,
    }


def serialize_detalle(det: Pedidodetalle):
    return {
        "id": det.id,
        "producto_id": det.producto_id,
        "nombre": det.producto.nombre if det.producto else "",
        "precio": float(det.precio),
        "cantidad": det.cantidad,
        "subtotal": float(det.subtotal),
        "imagen": (
            f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{det.producto.fotoprincipal}"
            if det.producto and det.producto.fotoprincipal else None
        )
    }

# ----------------------------------------------------------------------
# 📌 1. LISTAR PEDIDOS DE UN USUARIO
# ----------------------------------------------------------------------

@router.get("/listar/{usuario_id}")
def listar_pedidos(usuario_id: int, db: Session = Depends(get_db)):

    pedidos = (
        db.query(Pedido)
        .options(joinedload(Pedido.estadogeneral))
        .filter(Pedido.usuario_id == usuario_id)
        .order_by(Pedido.fecha.desc())
        .all()
    )

    return [serialize_pedido(p) for p in pedidos]


# ----------------------------------------------------------------------
# 📌 2. OBTENER PEDIDO COMPLETO (CON DETALLES)
# ----------------------------------------------------------------------

@router.get("/obtener/{pedido_id}")
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):

    pedido = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.estadogeneral),
            joinedload(Pedido.pedidodetalle)
                .joinedload(Pedidodetalle.producto),
        )
        .filter(Pedido.id == pedido_id)
        .first()
    )

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    detalles = [serialize_detalle(d) for d in pedido.pedidodetalle]

    return {
        "pedido": serialize_pedido(pedido),
        "detalles": detalles
    }


# ----------------------------------------------------------------------
# 📌 3. LISTAR SOLO DETALLES DE UN PEDIDO
# ----------------------------------------------------------------------

@router.get("/detalle/{pedido_id}")
def listar_detalles(pedido_id: int, db: Session = Depends(get_db)):

    detalles = (
        db.query(Pedidodetalle)
        .options(joinedload(Pedidodetalle.producto))
        .filter(Pedidodetalle.pedido_id == pedido_id)
        .all()
    )

    return [serialize_detalle(d) for d in detalles]
