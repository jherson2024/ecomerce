from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Etiqueta(Base):
    __tablename__ = 'etiqueta'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)

    productoetiqueta: Mapped[list['Productoetiqueta']] = relationship('Productoetiqueta', back_populates='etiqueta')
