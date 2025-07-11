from sqlalchemy import Column, Integer, String, Date, Numeric
from .database import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    produto = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_venda = Column(Date, nullable=False)
    vendedor = Column(String(100), nullable=False)
    regiao = Column(String(50), nullable=False)
