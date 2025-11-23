from typing import Optional
import datetime
import decimal

from sqlalchemy import CHAR, DECIMAL, Date, DateTime, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = 'categoria'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))

    producto: Mapped[list['Producto']] = relationship('Producto', back_populates='categoria')


class Estadogeneral(Base):
    __tablename__ = 'estadogeneral'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)

    carrito: Mapped[list['Carrito']] = relationship('Carrito', back_populates='estadogeneral')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='estadogeneral')
    envio: Mapped[list['Envio']] = relationship('Envio', back_populates='estadogeneral')
    pago: Mapped[list['Pago']] = relationship('Pago', back_populates='estadogeneral')


class Etiqueta(Base):
    __tablename__ = 'etiqueta'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)

    productoetiqueta: Mapped[list['Productoetiqueta']] = relationship('Productoetiqueta', back_populates='etiqueta')


class Pasarelapago(Base):
    __tablename__ = 'pasarelapago'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    apikey: Mapped[str] = mapped_column(String(100), nullable=False)
    urlbase: Mapped[str] = mapped_column(String(200), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))
    logo: Mapped[Optional[str]] = mapped_column(String(200))

    metodopago: Mapped[list['Metodopago']] = relationship('Metodopago', back_populates='pasarelapago')


class Provincia(Base):
    __tablename__ = 'provincia'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)

    distrito: Mapped[list['Distrito']] = relationship('Distrito', back_populates='provincia')


class Rol(Base):
    __tablename__ = 'rol'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))

    usuario: Mapped[list['Usuario']] = relationship('Usuario', back_populates='rol')


class Transportista(Base):
    __tablename__ = 'transportista'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(60))

    envio: Mapped[list['Envio']] = relationship('Envio', back_populates='transportista')


class Distrito(Base):
    __tablename__ = 'distrito'
    __table_args__ = (
        ForeignKeyConstraint(['provincia_id'], ['provincia.id'], name='distrito_ibfk_1'),
        Index('nombre', 'nombre', unique=True),
        Index('provincia_id', 'provincia_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    provincia_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)

    provincia: Mapped['Provincia'] = relationship('Provincia', back_populates='distrito')
    vendedor: Mapped[list['Vendedor']] = relationship('Vendedor', back_populates='distrito')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='distrito')


class Metodopago(Base):
    __tablename__ = 'metodopago'
    __table_args__ = (
        ForeignKeyConstraint(['pasarelapago_id'], ['pasarelapago.id'], name='metodopago_ibfk_1'),
        Index('nombre', 'nombre', unique=True),
        Index('pasarelapago_id', 'pasarelapago_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    soportaqr: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    pasarelapago_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))

    pasarelapago: Mapped['Pasarelapago'] = relationship('Pasarelapago', back_populates='metodopago')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='metodopago')
    pago: Mapped[list['Pago']] = relationship('Pago', back_populates='metodopago')


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        ForeignKeyConstraint(['rol_id'], ['rol.id'], name='usuario_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('rol_id', 'rol_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    clave: Mapped[str] = mapped_column(String(60), nullable=False)
    rol_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))

    rol: Mapped['Rol'] = relationship('Rol', back_populates='usuario')
    carrito: Mapped[list['Carrito']] = relationship('Carrito', back_populates='usuario')
    vendedor: Mapped[list['Vendedor']] = relationship('Vendedor', back_populates='usuario')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='usuario')
    resena: Mapped[list['Resena']] = relationship('Resena', back_populates='usuario')


class Carrito(Base):
    __tablename__ = 'carrito'
    __table_args__ = (
        ForeignKeyConstraint(['estadogeneral_id'], ['estadogeneral.id'], name='carrito_ibfk_2'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='carrito_ibfk_1'),
        Index('estadogeneral_id', 'estadogeneral_id'),
        Index('usuario_id', 'usuario_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    fechacreacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estadogeneral_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    estadogeneral: Mapped['Estadogeneral'] = relationship('Estadogeneral', back_populates='carrito')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='carrito')
    carritodetalle: Mapped[list['Carritodetalle']] = relationship('Carritodetalle', back_populates='carrito')


class Vendedor(Base):
    __tablename__ = 'vendedor'
    __table_args__ = (
        ForeignKeyConstraint(['distrito_id'], ['distrito.id'], name='vendedor_ibfk_2'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='vendedor_ibfk_1'),
        Index('distrito_id', 'distrito_id'),
        Index('usuario_id', 'usuario_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombretienda: Mapped[str] = mapped_column(String(60), nullable=False)
    distrito_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    logo: Mapped[Optional[str]] = mapped_column(String(200))

    distrito: Mapped['Distrito'] = relationship('Distrito', back_populates='vendedor')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='vendedor')
    colecciontienda: Mapped[list['Colecciontienda']] = relationship('Colecciontienda', back_populates='vendedor')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='vendedor')
    politicatienda: Mapped[list['Politicatienda']] = relationship('Politicatienda', back_populates='vendedor')
    producto: Mapped[list['Producto']] = relationship('Producto', back_populates='vendedor')


class Colecciontienda(Base):
    __tablename__ = 'colecciontienda'
    __table_args__ = (
        ForeignKeyConstraint(['vendedor_id'], ['vendedor.id'], name='colecciontienda_ibfk_1'),
        Index('nombre', 'nombre', unique=True),
        Index('vendedor_id', 'vendedor_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    vendedor_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))

    vendedor: Mapped['Vendedor'] = relationship('Vendedor', back_populates='colecciontienda')
    producto: Mapped[list['Producto']] = relationship('Producto', back_populates='colecciontienda')


class Pedido(Base):
    __tablename__ = 'pedido'
    __table_args__ = (
        ForeignKeyConstraint(['distrito_id'], ['distrito.id'], name='pedido_ibfk_3'),
        ForeignKeyConstraint(['estadogeneral_id'], ['estadogeneral.id'], name='pedido_ibfk_2'),
        ForeignKeyConstraint(['metodopago_id'], ['metodopago.id'], name='pedido_ibfk_4'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='pedido_ibfk_1'),
        ForeignKeyConstraint(['vendedor_id'], ['vendedor.id'], name='pedido_ibfk_5'),
        Index('distrito_id', 'distrito_id'),
        Index('estadogeneral_id', 'estadogeneral_id'),
        Index('metodopago_id', 'metodopago_id'),
        Index('usuario_id', 'usuario_id'),
        Index('vendedor_id', 'vendedor_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estadogeneral_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    distrito_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    direccionentrega: Mapped[str] = mapped_column(String(100), nullable=False)
    metodopago_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    vendedor_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    referencia: Mapped[Optional[str]] = mapped_column(String(150))

    distrito: Mapped['Distrito'] = relationship('Distrito', back_populates='pedido')
    estadogeneral: Mapped['Estadogeneral'] = relationship('Estadogeneral', back_populates='pedido')
    metodopago: Mapped['Metodopago'] = relationship('Metodopago', back_populates='pedido')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='pedido')
    vendedor: Mapped['Vendedor'] = relationship('Vendedor', back_populates='pedido')
    envio: Mapped[list['Envio']] = relationship('Envio', back_populates='pedido')
    pago: Mapped[list['Pago']] = relationship('Pago', back_populates='pedido')
    pedidodetalle: Mapped[list['Pedidodetalle']] = relationship('Pedidodetalle', back_populates='pedido')


class Politicatienda(Base):
    __tablename__ = 'politicatienda'
    __table_args__ = (
        ForeignKeyConstraint(['vendedor_id'], ['vendedor.id'], name='politicatienda_ibfk_1'),
        Index('vendedor_id', 'vendedor_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    vendedor_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    fechaactualizacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    politicaenvio: Mapped[Optional[str]] = mapped_column(Text)
    politicadevolucion: Mapped[Optional[str]] = mapped_column(Text)
    politicaprivacidad: Mapped[Optional[str]] = mapped_column(Text)

    vendedor: Mapped['Vendedor'] = relationship('Vendedor', back_populates='politicatienda')


class Envio(Base):
    __tablename__ = 'envio'
    __table_args__ = (
        ForeignKeyConstraint(['estadogeneral_id'], ['estadogeneral.id'], name='envio_ibfk_3'),
        ForeignKeyConstraint(['pedido_id'], ['pedido.id'], name='envio_ibfk_1'),
        ForeignKeyConstraint(['transportista_id'], ['transportista.id'], name='envio_ibfk_2'),
        Index('codigoseguimiento', 'codigoseguimiento', unique=True),
        Index('estadogeneral_id', 'estadogeneral_id'),
        Index('pedido_id', 'pedido_id'),
        Index('transportista_id', 'transportista_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    transportista_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estadogeneral_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    fechaenvio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    codigoseguimiento: Mapped[Optional[str]] = mapped_column(String(60))
    fechaentrega: Mapped[Optional[datetime.date]] = mapped_column(Date)
    urlseguimiento: Mapped[Optional[str]] = mapped_column(String(200))

    estadogeneral: Mapped['Estadogeneral'] = relationship('Estadogeneral', back_populates='envio')
    pedido: Mapped['Pedido'] = relationship('Pedido', back_populates='envio')
    transportista: Mapped['Transportista'] = relationship('Transportista', back_populates='envio')


class Pago(Base):
    __tablename__ = 'pago'
    __table_args__ = (
        ForeignKeyConstraint(['estadogeneral_id'], ['estadogeneral.id'], name='pago_ibfk_3'),
        ForeignKeyConstraint(['metodopago_id'], ['metodopago.id'], name='pago_ibfk_2'),
        ForeignKeyConstraint(['pedido_id'], ['pedido.id'], name='pago_ibfk_1'),
        Index('estadogeneral_id', 'estadogeneral_id'),
        Index('metodopago_id', 'metodopago_id'),
        Index('pedido_id', 'pedido_id', unique=True),
        Index('transaccionid', 'transaccionid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    metodopago_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    monto: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estadogeneral_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    urlpasarela: Mapped[str] = mapped_column(String(200), nullable=False)
    transaccionid: Mapped[Optional[str]] = mapped_column(String(60))

    estadogeneral: Mapped['Estadogeneral'] = relationship('Estadogeneral', back_populates='pago')
    metodopago: Mapped['Metodopago'] = relationship('Metodopago', back_populates='pago')
    pedido: Mapped['Pedido'] = relationship('Pedido', back_populates='pago')


class Producto(Base):
    __tablename__ = 'producto'
    __table_args__ = (
        ForeignKeyConstraint(['categoria_id'], ['categoria.id'], name='producto_ibfk_1'),
        ForeignKeyConstraint(['colecciontienda_id'], ['colecciontienda.id'], name='producto_ibfk_3'),
        ForeignKeyConstraint(['vendedor_id'], ['vendedor.id'], name='producto_ibfk_2'),
        Index('categoria_id', 'categoria_id'),
        Index('colecciontienda_id', 'colecciontienda_id'),
        Index('nombre', 'nombre', unique=True),
        Index('vendedor_id', 'vendedor_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    categoria_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    vendedor_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    colecciontienda_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    activodescuento: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    fotoprincipal: Mapped[Optional[str]] = mapped_column(String(200))
    descuento: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    fechainiciodescuento: Mapped[Optional[datetime.date]] = mapped_column(Date)
    fechafindescuento: Mapped[Optional[datetime.date]] = mapped_column(Date)

    categoria: Mapped['Categoria'] = relationship('Categoria', back_populates='producto')
    colecciontienda: Mapped['Colecciontienda'] = relationship('Colecciontienda', back_populates='producto')
    vendedor: Mapped['Vendedor'] = relationship('Vendedor', back_populates='producto')
    carritodetalle: Mapped[list['Carritodetalle']] = relationship('Carritodetalle', back_populates='producto')
    pedidodetalle: Mapped[list['Pedidodetalle']] = relationship('Pedidodetalle', back_populates='producto')
    productoetiqueta: Mapped[list['Productoetiqueta']] = relationship('Productoetiqueta', back_populates='producto')
    productoopcion: Mapped[list['Productoopcion']] = relationship('Productoopcion', back_populates='producto')
    resena: Mapped[list['Resena']] = relationship('Resena', back_populates='producto')


class Carritodetalle(Base):
    __tablename__ = 'carritodetalle'
    __table_args__ = (
        ForeignKeyConstraint(['carrito_id'], ['carrito.id'], name='carritodetalle_ibfk_1'),
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='carritodetalle_ibfk_2'),
        Index('carrito_id', 'carrito_id'),
        Index('producto_id', 'producto_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    carrito_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    carrito: Mapped['Carrito'] = relationship('Carrito', back_populates='carritodetalle')
    producto: Mapped['Producto'] = relationship('Producto', back_populates='carritodetalle')


class Pedidodetalle(Base):
    __tablename__ = 'pedidodetalle'
    __table_args__ = (
        ForeignKeyConstraint(['pedido_id'], ['pedido.id'], name='pedidodetalle_ibfk_1'),
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='pedidodetalle_ibfk_2'),
        Index('pedido_id', 'pedido_id'),
        Index('producto_id', 'producto_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    precio: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    pedido: Mapped['Pedido'] = relationship('Pedido', back_populates='pedidodetalle')
    producto: Mapped['Producto'] = relationship('Producto', back_populates='pedidodetalle')
    opcionpedido: Mapped[list['Opcionpedido']] = relationship('Opcionpedido', back_populates='pedidodetalle')


class Productoetiqueta(Base):
    __tablename__ = 'productoetiqueta'
    __table_args__ = (
        ForeignKeyConstraint(['etiqueta_id'], ['etiqueta.id'], name='productoetiqueta_ibfk_2'),
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='productoetiqueta_ibfk_1'),
        Index('etiqueta_id', 'etiqueta_id'),
        Index('producto_id', 'producto_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    etiqueta_id: Mapped[int] = mapped_column(BIGINT, nullable=False)

    etiqueta: Mapped['Etiqueta'] = relationship('Etiqueta', back_populates='productoetiqueta')
    producto: Mapped['Producto'] = relationship('Producto', back_populates='productoetiqueta')


class Productoopcion(Base):
    __tablename__ = 'productoopcion'
    __table_args__ = (
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='productoopcion_ibfk_1'),
        Index('producto_id', 'producto_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    tipo: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    valor: Mapped[str] = mapped_column(String(60), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    detalle: Mapped[Optional[str]] = mapped_column(Text)
    imagen: Mapped[Optional[str]] = mapped_column(String(200))

    producto: Mapped['Producto'] = relationship('Producto', back_populates='productoopcion')
    opcionpedido: Mapped[list['Opcionpedido']] = relationship('Opcionpedido', back_populates='productoopcion')


class Resena(Base):
    __tablename__ = 'resena'
    __table_args__ = (
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='resena_ibfk_1'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='resena_ibfk_2'),
        Index('producto_id', 'producto_id'),
        Index('usuario_id', 'usuario_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    usuario_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    puntuacion: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    respuestavendedor: Mapped[Optional[str]] = mapped_column(Text)

    producto: Mapped['Producto'] = relationship('Producto', back_populates='resena')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='resena')


class Opcionpedido(Base):
    __tablename__ = 'opcionpedido'
    __table_args__ = (
        ForeignKeyConstraint(['pedidodetalle_id'], ['pedidodetalle.id'], name='opcionpedido_ibfk_1'),
        ForeignKeyConstraint(['productoopcion_id'], ['productoopcion.id'], name='opcionpedido_ibfk_2'),
        Index('pedidodetalle_id', 'pedidodetalle_id', unique=True),
        Index('productoopcion_id', 'productoopcion_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    pedidodetalle_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    productoopcion_id: Mapped[int] = mapped_column(BIGINT, nullable=False)

    pedidodetalle: Mapped['Pedidodetalle'] = relationship('Pedidodetalle', back_populates='opcionpedido')
    productoopcion: Mapped['Productoopcion'] = relationship('Productoopcion', back_populates='opcionpedido')
