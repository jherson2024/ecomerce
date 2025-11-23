from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
