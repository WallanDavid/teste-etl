from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, crud, etl
import pandas as pd
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vendas", status_code=201)
def criar_venda(venda: dict, db: Session = Depends(get_db)):
    return crud.criar_venda(db, venda)

@app.get("/vendas")
def listar(db: Session = Depends(get_db)):
    return crud.listar_vendas(db)

@app.get("/vendas/{venda_id}")
def buscar(venda_id: int, db: Session = Depends(get_db)):
    venda = crud.buscar_venda(db, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@app.put("/vendas/{venda_id}")
def atualizar(venda_id: int, dados: dict, db: Session = Depends(get_db)):
    venda = crud.atualizar_venda(db, venda_id, dados)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@app.delete("/vendas/{venda_id}")
def deletar(venda_id: int, db: Session = Depends(get_db)):
    if not crud.deletar_venda(db, venda_id):
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"ok": True}

@app.post("/etl/importar-csv")
def importar(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = etl.processar_csv(file.file.read())
    for _, linha in df.iterrows():
        crud.criar_venda(db, linha.to_dict())
    return {"msg": "Importado com sucesso"}

@app.get("/etl/relatorio-mensal")
def relatorio(mes: str, db: Session = Depends(get_db)):
    vendas = crud.listar_vendas(db)
    df = pd.DataFrame([v.__dict__ for v in vendas])
    df = df.drop("_sa_instance_state", axis=1)
    return etl.gerar_relatorio_mensal(df, mes)

@app.get("/etl/exportar-dados")
def exportar(formato: str = "csv", db: Session = Depends(get_db)):
    vendas = crud.listar_vendas(db)
    df = pd.DataFrame([v.__dict__ for v in vendas])
    df = df.drop("_sa_instance_state", axis=1)

    if formato == "csv":
        path = "data/export.csv"
        df.to_csv(path, index=False)
        return {"arquivo": path}
    else:
        return df.to_dict(orient="records")
