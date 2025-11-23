from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from decimal import Decimal
import datetime

from core.globals import (
    IMAGENES_PRODUCTO_DIR,
    IMAGENES_TIENDA_LOGO_DIR,
    URL_SERVER,
    IMAGENES_QR_DIR
)

from core.imports import get_db
from utils.keygen import generate_uint64_key

from models import (
    Carrito, Carritodetalle, Pedido, Pedidodetalle,
    Metodopago, Distrito, Pago, Producto, Opcionpedido
)

# 🎯 ESTADOS
from constants.estados import (
    PEDIDO_PENDIENTE_PAGO,
    PAGO_PENDIENTE
)

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout / Pago"]
)


class CheckoutRequest(BaseModel):
    usuario_id: int
    metodopago_id: int
    distrito_id: int
    direccion: str
    referencia: str | None = None


class CheckoutResponse(BaseModel):
    mensaje: str
    pedido_id: str
    url_pago: str
    qr_imagen: str | None = None


# ------------------------------------------------------------------
# 🔥 CREAR PEDIDO + DETALLES + PAGO PENDIENTE
# ------------------------------------------------------------------
@router.post("/procesar", response_model=CheckoutResponse)
def procesar_pago(data: CheckoutRequest, db: Session = Depends(get_db)):

    # 1. Obtener carrito
    carrito = db.query(Carrito).filter(
        Carrito.usuario_id == data.usuario_id
    ).first()

    if not carrito or len(carrito.carritodetalle) == 0:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    # 2. Validar distrito
    distrito = db.query(Distrito).filter(
        Distrito.id == data.distrito_id
    ).first()

    if not distrito:
        raise HTTPException(status_code=400, detail="Distrito inválido")

    # 3. Validar método de pago
    metodopago = db.query(Metodopago).filter(
        Metodopago.id == data.metodopago_id,
        Metodopago.estadoregistro == "A"
    ).first()

    if not metodopago:
        raise HTTPException(status_code=400, detail="Método de pago inválido")

    pasarela = metodopago.pasarelapago

    # 4. Crear pedido con estado: PENDIENTE_PAGO
    ahora = datetime.datetime.now()

    pedido = Pedido(
        id=int(generate_uint64_key()),
        usuario_id=data.usuario_id,
        total=carrito.total,
        estadogeneral_id=PEDIDO_PENDIENTE_PAGO,   # CORRECTO
        fecha=ahora,
        distrito_id=data.distrito_id,
        direccionentrega=data.direccion,
        metodopago_id=data.metodopago_id,
        vendedor_id=carrito.carritodetalle[0].producto.vendedor_id,
        referencia=data.referencia
    )
    db.add(pedido)

    # 5. Crear detalles del pedido
    for item in carrito.carritodetalle:
        ped_det = Pedidodetalle(
            id=int(generate_uint64_key()),
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio=item.precio,
            subtotal=item.subtotal
        )
        db.add(ped_det)

    # 6. Generar URL de pago simulada
    url_pago = f"{pasarela.urlbase}/checkout?monto={pedido.total}&pedido={pedido.id}"

    # 7. Crear pago con estado: PENDIENTE
    pago = Pago(
        id=int(generate_uint64_key()),
        pedido_id=pedido.id,
        metodopago_id=data.metodopago_id,
        monto=pedido.total,
        fecha=ahora,
        estadogeneral_id=PAGO_PENDIENTE,  # CORRECTO
        urlpasarela=url_pago,
        transaccionid=None
    )
    db.add(pago)

    # 8. Vaciar carrito
    db.query(Carritodetalle).filter(
        Carritodetalle.carrito_id == carrito.id
    ).delete(synchronize_session=False)

    carrito.total = Decimal("0.00")

    db.commit()
    db.refresh(pedido)
    db.refresh(pago)

    # 9. QR si existe
    qr_imagen = (
        f"{URL_SERVER}{IMAGENES_QR_DIR}{pasarela.logo}"
        if getattr(pasarela, "logo", None) else None
    )

    return {
        "mensaje": "Pedido creado correctamente",
        "pedido_id": str(pedido.id),
        "url_pago": pago.urlpasarela,
        "qr_imagen": qr_imagen
    }


# ------------------------------------------------------------------
# 🔥 OBTENER PEDIDO COMPLETO CON RELACIONES
# ------------------------------------------------------------------
@router.get("/pedido/{pedido_id}")
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):

    pedido = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.usuario),
            joinedload(Pedido.vendedor),
            joinedload(Pedido.distrito),
            joinedload(Pedido.metodopago)
                .joinedload(Metodopago.pasarelapago),
            joinedload(Pedido.pago),
            joinedload(Pedido.pedidodetalle)
                .joinedload(Pedidodetalle.producto),
            joinedload(Pedido.pedidodetalle)
                .joinedload(Pedidodetalle.opcionpedido)
                .joinedload(Opcionpedido.productoopcion),
            joinedload(Pedido.envio)
        )
        .filter(Pedido.id == pedido_id)
        .first()
    )

    if not pedido:
        raise HTTPException(404, "Pedido no encontrado")

    # -------- Productos --------
    productos = []
    for det in pedido.pedidodetalle:

        opciones = [
            {
                "nombre": op.productoopcion.nombre,
                "valor": op.productoopcion.valor
            } for op in det.opcionpedido
        ]

        productos.append({
            "producto_id": det.producto.id,
            "nombre": det.producto.nombre,
            "precio": float(det.precio),
            "cantidad": det.cantidad,
            "subtotal": float(det.subtotal),
            "imagen": (
                f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{det.producto.fotoprincipal}"
                if det.producto.fotoprincipal else None
            ),
            "opciones": opciones
        })

    # -------- Envío --------
    envio_data = None
    if pedido.envio:
        envio = pedido.envio[0]
        envio_data = {
            "fecha_envio": envio.fechaenvio,
            "estado": envio.estadogeneral.nombre,
            "transportista": envio.transportista.nombre,
            "codigo": envio.codigoseguimiento,
            "url": envio.urlseguimiento,
            "fecha_entrega": envio.fechaentrega
        }

    # -------- Respuesta final --------
    return {
        "pedido_id": str(pedido.id),
        "fecha": pedido.fecha,
        "total": float(pedido.total),
        "estado": pedido.estadogeneral.nombre,
        "direccion": pedido.direccionentrega,
        "referencia": pedido.referencia,
        "distrito": pedido.distrito.nombre,

        "usuario": {
            "id": pedido.usuario.id,
            "nombre": pedido.usuario.nombre,
            "email": pedido.usuario.email
        },

        "vendedor": {
            "id": pedido.vendedor.id,
            "nombre": pedido.vendedor.nombretienda,
            "logo": (
                f"{URL_SERVER}{IMAGENES_TIENDA_LOGO_DIR}{pedido.vendedor.logo}"
                if pedido.vendedor.logo else None
            )
        },
        "pago": {
            "estado": pedido.pago[0].estadogeneral.nombre,
            "url": pedido.pago[0].urlpasarela,
            "transaccionid": pedido.pago[0].transaccionid,
            "monto": float(pedido.pago[0].monto)
        } if pedido.pago else None,

        "metodopago": pedido.metodopago.nombre,
        "productos": productos,
        "envio": envio_data
    }
