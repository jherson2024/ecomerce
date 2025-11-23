from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Vendedor(Base):
    __tablename__ = 'vendedor'
    __table_args__ = (
        ForeignKeyConstraint(['distrito_id'], ['distrito.id'], name='vendedor_ibfk_2'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='vendedor_ibfk_1'),
        Index('distrito_id', 'distrito_id'),
        Index('usuario_id', 'usuario_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    nombretienda: Mapped[str] = mapped_column(String(60), nullable=False)
    distrito_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    logo: Mapped[Optional[str]] = mapped_column(String(200))

    distrito: Mapped['Distrito'] = relationship('Distrito', back_populates='vendedor')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='vendedor')
    colecciontienda: Mapped[list['Colecciontienda']] = relationship('Colecciontienda', back_populates='vendedor')
    pedido: Mapped[list['Pedido']] = relationship('Pedido', back_populates='vendedor')
    politicatienda: Mapped[list['Politicatienda']] = relationship('Politicatienda', back_populates='vendedor')
    producto: Mapped[list['Producto']] = relationship('Producto', back_populates='vendedor')
