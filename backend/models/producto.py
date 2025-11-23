from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
