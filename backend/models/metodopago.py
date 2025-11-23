from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
