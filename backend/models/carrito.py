from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
