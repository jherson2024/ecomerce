from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Colecciontienda(Base):
    __tablename__ = 'colecciontienda'
    __table_args__ = (
        ForeignKeyConstraint(['vendedor_id'], ['vendedor.id'], name='colecciontienda_ibfk_1'),
        Index('nombre', 'nombre', unique=True),
        Index('vendedor_id', 'vendedor_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    vendedor_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))

    vendedor: Mapped['Vendedor'] = relationship('Vendedor', back_populates='colecciontienda')
    producto: Mapped[list['Producto']] = relationship('Producto', back_populates='colecciontienda')
