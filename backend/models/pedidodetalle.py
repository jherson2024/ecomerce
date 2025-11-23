from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
