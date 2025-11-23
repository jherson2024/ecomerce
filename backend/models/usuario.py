from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        ForeignKeyConstraint(['rol_id'], ['rol.id'], name='usuario_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('rol_id', 'rol_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    clave: Mapped[str] = mapped_column(String(60), nullable=False)
    rol_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))

    rol: Mapped['Rol'] = relationship('Rol', back_populates='usuario')
    carrito: Mapped[list['Carrito']] = relationship('Carrito', back_populates='usuario')
    vendedor: Mapped[list['Vendedor']] = relationship('Vendedor', back_populates='usuario')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='usuario')
    resena: Mapped[list['Resena']] = relationship('Resena', back_populates='usuario')
