from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Rol(Base):
    __tablename__ = 'rol'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))

    usuario: Mapped[list['Usuario']] = relationship('Usuario', back_populates='rol')
