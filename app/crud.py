from sqlalchemy.orm import Session
from .models import Venda
from datetime import date

def criar_venda(db: Session, venda_data: dict):
    venda = Venda(**venda_data)
    db.add(venda)
    db.commit()
    db.refresh(venda)
    return venda

def listar_vendas(db: Session):
    return db.query(Venda).all()

def buscar_venda(db: Session, venda_id: int):
    return db.query(Venda).filter(Venda.id == venda_id).first()

def atualizar_venda(db: Session, venda_id: int, dados: dict):
    venda = buscar_venda(db, venda_id)
    if not venda:
        return None
    for chave, valor in dados.items():
        setattr(venda, chave, valor)
    db.commit()
    db.refresh(venda)
    return venda

def deletar_venda(db: Session, venda_id: int):
    venda = buscar_venda(db, venda_id)
    if not venda:
        return False
    db.delete(venda)
    db.commit()
    return True
