from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Provincia(Base):
    __tablename__ = 'provincia'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)

    distrito: Mapped[list['Distrito']] = relationship('Distrito', back_populates='provincia')
