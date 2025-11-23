from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Productoetiqueta(Base):
    __tablename__ = 'productoetiqueta'
    __table_args__ = (
        ForeignKeyConstraint(['etiqueta_id'], ['etiqueta.id'], name='productoetiqueta_ibfk_2'),
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='productoetiqueta_ibfk_1'),
        Index('etiqueta_id', 'etiqueta_id'),
        Index('producto_id', 'producto_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    etiqueta_id: Mapped[int] = mapped_column(BIGINT, nullable=False)

    etiqueta: Mapped['Etiqueta'] = relationship('Etiqueta', back_populates='productoetiqueta')
    producto: Mapped['Producto'] = relationship('Producto', back_populates='productoetiqueta')
