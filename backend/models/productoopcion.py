from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
