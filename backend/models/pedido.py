from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

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
