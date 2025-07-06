from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional


class VendaBase(BaseModel):
    produto: str = Field(..., max_length=100)
    categoria: str
    preco: float = Field(..., gt=0)
    quantidade: int = Field(..., gt=0)
    data_venda: date
    vendedor: str
    regiao: str

    @validator("data_venda")
    def data_nao_pode_ser_futura(cls, value):
        from datetime import date
        if value > date.today():
            raise ValueError("A data de venda não pode ser futura.")
        return value


class VendaCreate(VendaBase):
    pass


class VendaUpdate(BaseModel):
    produto: Optional[str] = Field(None, max_length=100)
    categoria: Optional[str]
    preco: Optional[float] = Field(None, gt=0)
    quantidade: Optional[int] = Field(None, gt=0)
    data_venda: Optional[date]
    vendedor: Optional[str]
    regiao: Optional[str]

    @validator("data_venda")
    def data_valida(cls, value):
        if value and value > date.today():
            raise ValueError("A data de venda não pode ser futura.")
        return value


class VendaResponse(VendaBase):
    id: int

    class Config:
        orm_mode = True
