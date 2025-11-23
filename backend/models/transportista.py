from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Transportista(Base):
    __tablename__ = 'transportista'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(60))

    envio: Mapped[list['Envio']] = relationship('Envio', back_populates='transportista')
