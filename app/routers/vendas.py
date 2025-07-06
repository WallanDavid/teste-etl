from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/vendas", status_code=201)
def criar_venda(venda: dict, db: Session = Depends(get_db)):
    return crud.criar_venda(db, venda)

@router.get("/vendas")
def listar(db: Session = Depends(get_db)):
    return crud.listar_vendas(db)

@router.get("/vendas/{venda_id}")
def buscar(venda_id: int, db: Session = Depends(get_db)):
    venda = crud.buscar_venda(db, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@router.put("/vendas/{venda_id}")
def atualizar(venda_id: int, dados: dict, db: Session = Depends(get_db)):
    venda = crud.atualizar_venda(db, venda_id, dados)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@router.delete("/vendas/{venda_id}")
def deletar(venda_id: int, db: Session = Depends(get_db)):
    if not crud.deletar_venda(db, venda_id):
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"ok": True}
