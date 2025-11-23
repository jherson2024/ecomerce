from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
