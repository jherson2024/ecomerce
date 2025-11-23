from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .base import Base

class Politicatienda(Base):
    __tablename__ = 'politicatienda'
    __table_args__ = (
        ForeignKeyConstraint(['vendedor_id'], ['vendedor.id'], name='politicatienda_ibfk_1'),
        Index('vendedor_id', 'vendedor_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    vendedor_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    fechaactualizacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estadoregistro: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    politicaenvio: Mapped[Optional[str]] = mapped_column(Text)
    politicadevolucion: Mapped[Optional[str]] = mapped_column(Text)
    politicaprivacidad: Mapped[Optional[str]] = mapped_column(Text)

    vendedor: Mapped['Vendedor'] = relationship('Vendedor', back_populates='politicatienda')
