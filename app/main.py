from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, crud, etl
import pandas as pd
import os

# Cria as tabelas no banco (executado na inicialização)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency para obter a sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: Criar venda
@app.post("/vendas", status_code=201)
def criar_venda(venda: dict, db: Session = Depends(get_db)):
    return crud.criar_venda(db, venda)

# Endpoint: Listar vendas
@app.get("/vendas")
def listar(db: Session = Depends(get_db)):
    return crud.listar_vendas(db)

# Endpoint: Buscar venda por ID
@app.get("/vendas/{venda_id}")
def buscar(venda_id: int, db: Session = Depends(get_db)):
    venda = crud.buscar_venda(db, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

# Endpoint: Atualizar venda
@app.put("/vendas/{venda_id}")
def atualizar(venda_id: int, dados: dict, db: Session = Depends(get_db)):
    venda = crud.atualizar_venda(db, venda_id, dados)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

# Endpoint: Deletar venda
@app.delete("/vendas/{venda_id}")
def deletar(venda_id: int, db: Session = Depends(get_db)):
    if not crud.deletar_venda(db, venda_id):
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"ok": True}

# Endpoint: Importar CSV (ETL)
@app.post("/etl/importar-csv")
def importar(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = etl.processar_csv(file.file.read())
    for _, linha in df.iterrows():
        crud.criar_venda(db, linha.to_dict())
    return {"msg": "Importado com sucesso"}

# Endpoint: Relatório mensal
@app.get("/etl/relatorio-mensal")
def relatorio(mes: str, db: Session = Depends(get_db)):
    vendas = crud.listar_vendas(db)
    if not vendas:
        return {
            "mes": mes,
            "total_vendas": 0.0,
            "total_itens": 0,
            "vendas_por_categoria": {},
            "top_vendedor": None
        }
    
    df = pd.DataFrame([v.__dict__ for v in vendas])
    if "_sa_instance_state" in df.columns:
        df.drop("_sa_instance_state", axis=1, inplace=True)

    return etl.gerar_relatorio_mensal(df, mes)

# Endpoint: Exportar dados
@app.get("/etl/exportar-dados")
def exportar(formato: str = "csv", db: Session = Depends(get_db)):
    vendas = crud.listar_vendas(db)
    df = pd.DataFrame([v.__dict__ for v in vendas])
    if "_sa_instance_state" in df.columns:
        df.drop("_sa_instance_state", axis=1, inplace=True)

    if formato == "csv":
        path = "data/export.csv"
        os.makedirs("data", exist_ok=True)
        df.to_csv(path, index=False)
        return {"arquivo": path}
    else:
        return df.to_dict(orient="records")
