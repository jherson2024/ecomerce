from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Pasarelapago(Base):
    __tablename__ = 'pasarelapago'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    apikey: Mapped[str] = mapped_column(String(100), nullable=False)
    urlbase: Mapped[str] = mapped_column(String(200), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))
    logo: Mapped[Optional[str]] = mapped_column(String(200))

    metodopago: Mapped[list['Metodopago']] = relationship('Metodopago', back_populates='pasarelapago')
