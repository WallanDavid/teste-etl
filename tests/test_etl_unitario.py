import pytest
import pandas as pd
from app.etl import processar_csv, gerar_relatorio_mensal

def test_processar_csv_valido():
    csv_data = """data_venda,produto,categoria,vendedor,preco,quantidade,regiao
2025-07-01,Notebook,Eletronicos,Ana,200.00,2,Sudeste
2025-07-02,Smartphone,Eletronicos,Carlos,300.00,1,Sudeste
2025-07-05,Quebra-Cabeca,Brinquedos,Ana,100.00,5,Sul
""".encode("utf-8")  # ✅ Corrigido: encode da string para evitar problemas com acento

    df = processar_csv(csv_data)
    assert not df.empty
    assert df.shape[0] == 3  # 3 linhas válidas
    assert pd.api.types.is_numeric_dtype(df['preco'])
    assert pd.api.types.is_numeric_dtype(df['quantidade'])

def test_processar_csv_com_dados_invalidos():
    csv_data = """data_venda,produto,categoria,vendedor,preco,quantidade,regiao
2025-08-01,Notebook,Eletronicos,Ana,-50.00,2,Sudeste
,Smartphone,Eletronicos,Carlos,300.00,1,Sudeste
""".encode("utf-8")

    df = processar_csv(csv_data)
    assert df.empty  # ✅ Nenhuma linha válida

def test_gerar_relatorio_mensal_valido():
    dados = {
        "data_venda": ["2025-07-01", "2025-07-02", "2025-07-05"],
        "produto": ["Notebook", "Smartphone", "Quebra-Cabeca"],
        "categoria": ["Eletronicos", "Eletronicos", "Brinquedos"],
        "vendedor": ["Ana", "Carlos", "Ana"],
        "preco": [200.00, 300.00, 100.00],
        "quantidade": [2, 1, 5],
        "regiao": ["Sudeste", "Sudeste", "Sul"]
    }
    df = pd.DataFrame(dados)
    relatorio = gerar_relatorio_mensal(df, "2025-07")

    assert relatorio["mes"] == "2025-07"
    assert relatorio["total_vendas"] == 1200.0  # 200*2 + 300*1 + 100*5
    assert relatorio["total_itens"] == 8
    assert relatorio["vendas_por_categoria"] == {
        "Eletronicos": 700.0,
        "Brinquedos": 500.0
    }
    assert relatorio["top_vendedor"] == "Ana"

def test_gerar_relatorio_mensal_sem_dados():
    df = pd.DataFrame(columns=[
        "data_venda", "produto", "categoria", "vendedor", "preco", "quantidade", "regiao"
    ])
    relatorio = gerar_relatorio_mensal(df, "2025-07")
    assert relatorio == {
        "mes": "2025-07",
        "total_vendas": 0.0,
        "total_itens": 0,
        "vendas_por_categoria": {},
        "top_vendedor": None
    }
