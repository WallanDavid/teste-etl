from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, etl
import pandas as pd
import os

router = APIRouter()

@router.post("/etl/importar-csv")
def importar_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = etl.processar_csv(file.file.read())
    for _, linha in df.iterrows():
        crud.criar_venda(db, linha.to_dict())
    return {"msg": "Importado com sucesso"}

@router.get("/etl/relatorio-mensal")
def relatorio_mensal(mes: str, db: Session = Depends(get_db)):
    vendas = crud.listar_vendas(db)
    if not vendas:
        return {"msg": "Nenhuma venda encontrada para gerar o relatório"}
    
    df = pd.DataFrame([v.__dict__ for v in vendas])
    df = df.drop("_sa_instance_state", axis=1)
    return etl.gerar_relatorio_mensal(df, mes)

@router.get("/etl/exportar-dados")
def exportar_dados(formato: str = "csv", db: Session = Depends(get_db)):
    vendas = crud.listar_vendas(db)
    df = pd.DataFrame([v.__dict__ for v in vendas])
    df = df.drop("_sa_instance_state", axis=1)

    if formato.lower() == "csv":
        path = os.path.join("data", "export.csv")
        os.makedirs("data", exist_ok=True)
        df.to_csv(path, index=False)
        return {"arquivo": path}
    elif formato.lower() == "json":
        return df.to_dict(orient="records")
    else:
        return {"erro": "Formato inválido. Use 'csv' ou 'json'."}
