import pytest
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_teste():
    """Simula um tempo de setup antes dos testes"""
    pass  # Se quiser manter o sleep(3), pode, mas TestClient não precisa disso.


def test_criar_e_buscar_venda():
    venda = {
        "produto": "Smartphone",
        "categoria": "Eletrônicos",
        "preco": 1999.90,
        "quantidade": 1,
        "data_venda": "2024-01-20",
        "vendedor": "Ana",
        "regiao": "Nordeste"
    }

    r = client.post("/vendas", json=venda)
    assert r.status_code == 201, f"Erro ao criar: {r.text}"
    venda_id = r.json().get("id")
    assert venda_id, "ID da venda não retornado"

    r = client.get(f"/vendas/{venda_id}")
    assert r.status_code == 200, f"Erro ao buscar: {r.text}"


def test_listar_vendas():
    r = client.get("/vendas")
    assert r.status_code == 200
    assert isinstance(r.json(), list), "Resposta não é lista"


def test_importar_csv():
    df = pd.DataFrame({
        'produto': ['Cadeira', 'Luminária'],
        'categoria': ['Casa', 'Casa'],
        'preco': [150.0, 80.0],
        'quantidade': [2, 3],
        'data_venda': ['2024-02-01', '2024-02-02'],
        'vendedor': ['Carlos', 'Marina'],
        'regiao': ['Sul', 'Centro-Oeste']
    })
    csv = df.to_csv(index=False).encode('utf-8')
    files = {'file': ('teste.csv', csv, 'text/csv')}

    r = client.post("/etl/importar-csv", files=files)
    assert r.status_code == 200, f"Erro ao importar CSV: {r.text}"


def test_relatorio_mensal():
    r = client.get("/etl/relatorio-mensal?mes=2024-02")
    assert r.status_code == 200
    data = r.json()
    assert "total_vendas" in data
    assert "vendas_por_categoria" in data
    assert "top_vendedor" in data
