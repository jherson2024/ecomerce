from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
