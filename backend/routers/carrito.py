from core.imports import *
from models import *
from pydantic import BaseModel
from utils.keygen import generate_uint64_key
from decimal import Decimal
router = APIRouter(
    prefix="/carrito",
    tags=["Carrito"]
)

# ============================
#  SCHEMAS
# ============================

class CarritoDetalleSchema(BaseModel):
    id: str
    producto_id: str
    nombre: str
    cantidad: int
    precio: float
    subtotal: float
    imagen: Optional[str]

class CarritoResponse(BaseModel):
    carrito_id: str
    usuario_id: str
    total: float
    detalles: List[CarritoDetalleSchema]


# ============================
#  OBTENER O CREAR CARRITO
# ============================

def obtener_o_crear_carrito(usuario_id: int, db: Session):
    carrito = (
        db.query(Carrito)
        .filter(Carrito.usuario_id == usuario_id)
        .first()
    )

    if not carrito:
        carrito = Carrito(
            id=int(generate_uint64_key()),
            usuario_id=usuario_id,
            estadogeneral_id=1,  # Ajustar según tu tabla
            fechacreacion=datetime.datetime.now(),
            total=Decimal("0.00")
        )
        db.add(carrito)
        db.commit()
        db.refresh(carrito)

    return carrito


# ============================
#  VER CARRITO
# ============================

@router.get("/obtener/{usuario_id}", response_model=CarritoResponse)
def obtener_carrito(usuario_id: int, db: Session = Depends(get_db)):
    carrito = obtener_o_crear_carrito(usuario_id, db)

    detalles = []
    for d in carrito.carritodetalle:
        imagen = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{d.producto.fotoprincipal}" if d.producto.fotoprincipal else None
        detalles.append({
            "id": str(d.id),
            "producto_id": str(d.producto_id),
            "nombre": d.producto.nombre,
            "cantidad": d.cantidad,
            "precio": float(d.precio),
            "subtotal": float(d.subtotal),
            "imagen": imagen
        })

    return {
        "carrito_id": str(carrito.id),
        "usuario_id": str(carrito.usuario_id),
        "total": float(carrito.total),
        "detalles": detalles
    }


# ============================
#  AGREGAR PRODUCTO
# ============================

@router.post("/agregar")
def agregar_producto(
    usuario_id: int = Query(...),
    producto_id: int = Query(...),
    cantidad: int = Query(..., ge=1),
    db: Session = Depends(get_db)
):
    carrito = obtener_o_crear_carrito(usuario_id, db)

    producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.estado == "A",
        Producto.stock > 0
    ).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no disponible")

    detalle = (
        db.query(Carritodetalle)
        .filter(
            Carritodetalle.carrito_id == carrito.id,
            Carritodetalle.producto_id == producto_id
        ).first()
    )

    if detalle:
        detalle.cantidad += cantidad
        detalle.subtotal = detalle.cantidad * detalle.precio
    else:
        detalle = Carritodetalle(
            id=int(generate_uint64_key()),
            carrito_id=carrito.id,
            producto_id=producto.id,
            cantidad=cantidad,
            precio=producto.precio,
            subtotal=producto.precio * cantidad
        )
        db.add(detalle)

    carrito.total = sum(d.subtotal for d in carrito.carritodetalle)

    db.commit()
    return {"mensaje": "Producto agregado al carrito"}


# ============================
#  ACTUALIZAR CANTIDAD
# ============================

@router.put("/actualizar/{detalle_id}")
def actualizar_cantidad(detalle_id: int, cantidad: int = Query(..., ge=1), db: Session = Depends(get_db)):
    detalle = db.query(Carritodetalle).filter(Carritodetalle.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    detalle.cantidad = cantidad
    detalle.subtotal = detalle.precio * cantidad

    carrito = db.query(Carrito).filter(Carrito.id == detalle.carrito_id).first()
    carrito.total = sum(d.subtotal for d in carrito.carritodetalle)

    db.commit()
    return {"mensaje": "Cantidad actualizada"}


# ============================
#  ELIMINAR PRODUCTO
# ============================

@router.delete("/eliminar/{detalle_id}")
def eliminar_producto(detalle_id: int, db: Session = Depends(get_db)):
    detalle = db.query(Carritodetalle).filter(Carritodetalle.id == detalle_id).first()

    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    carrito = db.query(Carrito).filter(Carrito.id == detalle.carrito_id).first()

    carrito.total -= detalle.subtotal
    db.delete(detalle)
    db.commit()

    return {"mensaje": "Producto eliminado del carrito"}


# ============================
#  VACIAR CARRITO
# ============================

@router.delete("/vaciar/{usuario_id}")
def vaciar_carrito(usuario_id: int, db: Session = Depends(get_db)):
    carrito = obtener_o_crear_carrito(usuario_id, db)

    db.query(Carritodetalle).filter(
        Carritodetalle.carrito_id == carrito.id
    ).delete(synchronize_session=False)

    carrito.total = Decimal("0.00")
    db.commit()

    return {"mensaje": "Carrito vaciado"}
