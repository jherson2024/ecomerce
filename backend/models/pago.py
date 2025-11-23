from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
