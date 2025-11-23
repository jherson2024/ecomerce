from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Envio(Base):
    __tablename__ = 'envio'
    __table_args__ = (
        ForeignKeyConstraint(['estadogeneral_id'], ['estadogeneral.id'], name='envio_ibfk_3'),
        ForeignKeyConstraint(['pedido_id'], ['pedido.id'], name='envio_ibfk_1'),
        ForeignKeyConstraint(['transportista_id'], ['transportista.id'], name='envio_ibfk_2'),
        Index('codigoseguimiento', 'codigoseguimiento', unique=True),
        Index('estadogeneral_id', 'estadogeneral_id'),
        Index('pedido_id', 'pedido_id'),
        Index('transportista_id', 'transportista_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    transportista_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estadogeneral_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    fechaenvio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    codigoseguimiento: Mapped[Optional[str]] = mapped_column(String(60))
    fechaentrega: Mapped[Optional[datetime.date]] = mapped_column(Date)
    urlseguimiento: Mapped[Optional[str]] = mapped_column(String(200))

    estadogeneral: Mapped['Estadogeneral'] = relationship('Estadogeneral', back_populates='envio')
    pedido: Mapped['Pedido'] = relationship('Pedido', back_populates='envio')
    transportista: Mapped['Transportista'] = relationship('Transportista', back_populates='envio')
