from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Distrito(Base):
    __tablename__ = 'distrito'
    __table_args__ = (
        ForeignKeyConstraint(['provincia_id'], ['provincia.id'], name='distrito_ibfk_1'),
        Index('nombre', 'nombre', unique=True),
        Index('provincia_id', 'provincia_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    provincia_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)

    provincia: Mapped['Provincia'] = relationship('Provincia', back_populates='distrito')
    vendedor: Mapped[list['Vendedor']] = relationship('Vendedor', back_populates='distrito')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='distrito')
