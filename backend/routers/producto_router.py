from core.imports import *
from models import *
from pydantic import BaseModel
from sqlalchemy import func
router = APIRouter(
    prefix="/producto",
    tags=["Producto"]
)
# === Modelo de respuesta ===
class ProductoListResponse(BaseModel):
    id: str
    nombre: str
    precio: float
    imagen: Optional[str]
    class Config:
        orm_mode = True
# === Listar productos activos por categoría ===
@router.get("/listar_por_categoria/{categoria_id}", response_model=List[ProductoListResponse])
def listar_productos_por_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    productos = (
        db.query(Producto)
        .filter(
            Producto.categoria_id == categoria_id,
            Producto.stock > 0,
            Producto.estado == "A"     # Solo activos
        )
        .limit(limit)
        .all()
    )
    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    return resultado

    # === Modelos de respuesta ===
class ProductoListResponse(BaseModel):
    id: str
    nombre: str
    precio: float
    imagen: Optional[str]

    class Config:
        orm_mode = True


class CategoriaListResponse(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str]

    class Config:
        orm_mode = True


# === 1️⃣ Listar productos disponibles (stock > 0) ===
@router.get("/listar_disponibles", response_model=List[ProductoListResponse])
def listar_productos_disponibles(
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    productos = (
        db.query(Producto)
        .filter(Producto.stock > 0)
        .limit(limit)
        .all()
    )

    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    return resultado


# === 2️⃣ Listar productos activos por categoría ===
@router.get("/listar_por_categoria/{categoria_id}", response_model=List[ProductoListResponse])
def listar_productos_por_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    productos = (
        db.query(Producto)
        .filter(
            Producto.categoria_id == categoria_id,
            Producto.stock > 0,
            Producto.estado == "A"
        )
        .limit(limit)
        .all()
    )

    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    return resultado


# === 3️⃣ Listar todas las categorías ===
@router.get("/listar_categorias", response_model=List[CategoriaListResponse])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()

    resultado = []
    for c in categorias:
        resultado.append({
            "id": str(c.id),
            "nombre": c.nombre,
            "descripcion": c.descripcion
        })

    return resultado
# === 4️⃣ Listar productos de una tienda específica ===
@router.get("/listar_por_tienda/{vendedor_id}", response_model=List[ProductoListResponse])
def listar_productos_por_tienda(
    vendedor_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    productos = (
        db.query(Producto)
        .filter(
            Producto.vendedor_id == vendedor_id,
            Producto.stock > 0,
            Producto.estado == "A"
        )
        .limit(limit)
        .all()
    )

    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    return resultado
# === 5️⃣ Listar productos de una tienda por categoría ===
@router.get("/listar_por_tienda_categoria/{vendedor_id}/{categoria_id}", response_model=List[ProductoListResponse])
def listar_productos_por_tienda_categoria(
    vendedor_id: int,
    categoria_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    productos = (
        db.query(Producto)
        .filter(
            Producto.vendedor_id == vendedor_id,
            Producto.categoria_id == categoria_id,
            Producto.stock > 0,
            Producto.estado == "A"
        )
        .limit(limit)
        .all()
    )

    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    return resultado
@router.get("/detalle/{producto_id}")
def ver_detalle_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = (
        db.query(Producto)
        .filter(Producto.id == producto_id, Producto.estado == "A")
        .first()
    )
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o inactivo")

    # --- Imagen principal ---
    imagen_url = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{producto.fotoprincipal}" if producto.fotoprincipal else None

    # --- Información del vendedor y políticas ---
    vendedor = producto.vendedor
    tienda_info = None
    if vendedor:
        politicas = vendedor.politicatienda[0] if vendedor.politicatienda else None
        tienda_info = {
            "id": str(vendedor.id),
            "nombre_tienda": vendedor.nombretienda,
            "descripcion": vendedor.descripcion,
            "logo": f"{URL_SERVER}{IMAGENES_TIENDA_LOGO_DIR}{vendedor.logo}" if vendedor.logo else None,
            "ubicacion": f"{vendedor.distrito.nombre}, {vendedor.distrito.provincia.nombre}" if vendedor.distrito else None,
            "politicas": {
                "envio": politicas.politicaenvio if politicas else None,
                "devolucion": politicas.politicadevolucion if politicas else None,
                "privacidad": politicas.politicaprivacidad if politicas else None,
                "ultima_actualizacion": politicas.fechaactualizacion.strftime("%Y-%m-%d") if politicas else None
            }
        }

    # --- Variaciones del producto ---
    opciones = []
    for o in producto.productoopcion:
        if o.estadoregistro == "A":
            opciones.append({
                "id": str(o.id),
                "nombre": o.nombre,
                "valor": o.valor,
                "tipo": o.tipo,
                "detalle": o.detalle,
                "imagen": f"{URL_SERVER}{IMAGENES_PRODUCTO_OPCION_DIR}{o.imagen}" if o.imagen else None
            })

    # --- Reseñas del producto ---
    reseñas = []
    for r in producto.resena:
        if r.estado == "A":
            reseñas.append({
                "usuario": r.usuario.nombre if r.usuario else "Anónimo",
                "puntuacion": r.puntuacion,
                "comentario": r.comentario,
                "fecha": r.fecha.strftime("%Y-%m-%d"),
                "respuesta_vendedor": r.respuestavendedor
            })
    promedio_puntuacion = round(sum(r["puntuacion"] for r in reseñas) / len(reseñas), 1) if reseñas else 0

    # --- Cantidad de reseñas por puntuación ---
    distribucion_puntuacion = {i: 0 for i in range(1, 6)}
    for r in reseñas:
        distribucion_puntuacion[r["puntuacion"]] += 1

    # --- Descuento activo ---
    descuento_activo = None
    if producto.activodescuento and producto.fechainiciodescuento and producto.fechafindescuento:
        hoy = datetime.date.today()
        if producto.fechainiciodescuento <= hoy <= producto.fechafindescuento:
            descuento_activo = {
                "valor": float(producto.descuento or 0),
                "inicio": producto.fechainiciodescuento.strftime("%Y-%m-%d"),
                "fin": producto.fechafindescuento.strftime("%Y-%m-%d")
            }

    # --- En cuántos carritos está ---
    carritos_count = (
        db.query(func.count(Carritodetalle.id))
        .join(Carrito, Carritodetalle.carrito_id == Carrito.id)
        .filter(Carritodetalle.producto_id == producto.id)
        .scalar()
    )

    # --- Productos similares (por categoría o etiquetas) ---
    etiquetas_ids = [pe.etiqueta_id for pe in producto.productoetiqueta]
    similares_query = db.query(Producto).filter(
        Producto.estado == "A",
        Producto.stock > 0,
        Producto.id != producto.id
    )
    if etiquetas_ids:
        similares_query = similares_query.join(Productoetiqueta).filter(Productoetiqueta.etiqueta_id.in_(etiquetas_ids))
    else:
        similares_query = similares_query.filter(Producto.categoria_id == producto.categoria_id)

    similares = [
        {
            "id": str(s.id),
            "nombre": s.nombre,
            "precio": float(s.precio),
            "imagen": f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{s.fotoprincipal}" if s.fotoprincipal else None
        }
        for s in similares_query.limit(6).all()
    ]

    # --- Construir respuesta final ---
    detalle = {
        "id": str(producto.id),
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": float(producto.precio),
        "stock": producto.stock,
        "categoria": producto.categoria.nombre if producto.categoria else None,
        "imagen": imagen_url,
        "descuento_activo": descuento_activo,
        "tienda": tienda_info,
        "opciones": opciones,
        "reseñas": reseñas,
        "promedio_puntuacion": promedio_puntuacion,
        "distribucion_puntuacion": distribucion_puntuacion,
        "en_carritos": carritos_count,
        "coleccion": producto.colecciontienda.nombre if producto.colecciontienda else None,
        "productos_similares": similares,
    }

    return detalle

@router.get("/listar_por_coleccion/{coleccion_id}", response_model=List[ProductoListResponse])
def listar_productos_por_coleccion(
    coleccion_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    productos = (
        db.query(Producto)
        .filter(
            Producto.colecciontienda_id == coleccion_id,
            Producto.estado == "A",
            Producto.estadoregistro == "A",
            Producto.stock > 0
        )
        .limit(limit)
        .all()
    )

    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    return resultado
# === 1️⃣1️⃣ Listar colecciones activas de una tienda ===
@router.get("/listar_colecciones_por_tienda/{vendedor_id}")
def listar_colecciones_por_tienda(vendedor_id: int, db: Session = Depends(get_db)):
    colecciones = (
        db.query(Colecciontienda)
        .filter(
            Colecciontienda.vendedor_id == vendedor_id,
            Colecciontienda.estadoregistro == "A"
        )
        .all()
    )

    if not colecciones:
        raise HTTPException(status_code=404, detail="No se encontraron colecciones activas para esta tienda")

    resultado = []
    for c in colecciones:
        resultado.append({
            "id": str(c.id),
            "nombre": c.nombre,
            "descripcion": c.descripcion,
            "tienda": c.vendedor.nombretienda if c.vendedor else None,
            "tienda_logo": f"{URL_SERVER}{c.vendedor.logo}" if c.vendedor and c.vendedor.logo else None
        })

    return resultado
# === 1️⃣2️⃣ Buscar productos por palabra clave (nombre, descripción, categoría o etiqueta) ===
@router.get("/buscar", response_model=List[ProductoListResponse])
def buscar_productos(
    q: str = Query(..., min_length=2, description="Palabra clave a buscar"),
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=200, description="Cantidad máxima de productos a mostrar")
):
    # Subconsultas para encontrar coincidencias por categoría o etiqueta
    categorias_ids = (
        db.query(Categoria.id)
        .filter(Categoria.nombre.ilike(f"%{q}%"))
        .subquery()
    )

    etiquetas_ids = (
        db.query(Productoetiqueta.producto_id)
        .join(Etiqueta, Productoetiqueta.etiqueta_id == Etiqueta.id)
        .filter(Etiqueta.nombre.ilike(f"%{q}%"))
        .subquery()
    )

    # Consulta principal de productos
    productos = (
        db.query(Producto)
        .filter(
            Producto.estado == "A",
            Producto.estadoregistro == "A",
            Producto.stock > 0,
            (
                Producto.nombre.ilike(f"%{q}%") |
                Producto.descripcion.ilike(f"%{q}%") |
                Producto.categoria_id.in_(categorias_ids) |
                Producto.id.in_(etiquetas_ids)
            )
        )
        .limit(limit)
        .all()
    )

    # Construcción del resultado final
    resultado = []
    for p in productos:
        imagen_url = f"{URL_SERVER}{IMAGENES_PRODUCTO_DIR}{p.fotoprincipal}" if p.fotoprincipal else None
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre,
            "precio": float(p.precio),
            "imagen": imagen_url
        })

    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron productos que coincidan con la búsqueda")

    return resultado
