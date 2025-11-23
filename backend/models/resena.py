from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Resena(Base):
    __tablename__ = 'resena'
    __table_args__ = (
        ForeignKeyConstraint(['producto_id'], ['producto.id'], name='resena_ibfk_1'),
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='resena_ibfk_2'),
        Index('producto_id', 'producto_id'),
        Index('usuario_id', 'usuario_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    producto_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    usuario_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    puntuacion: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    respuestavendedor: Mapped[Optional[str]] = mapped_column(Text)

    producto: Mapped['Producto'] = relationship('Producto', back_populates='resena')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='resena')
