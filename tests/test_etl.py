import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_etl_relatorio_mensal_com_csv():
    # CSV de teste em memória com colunas completas
    csv_data = """data_venda,produto,categoria,vendedor,preco,quantidade,regiao
2025-07-01,Notebook,Eletrônicos,Ana,200.00,2,Sudeste
2025-07-02,Smartphone,Eletrônicos,Carlos,300.00,1,Sudeste
2025-07-05,Quebra-Cabeça,Brinquedos,Ana,100.00,5,Sul
"""

    # 1. Envia o CSV
    response_upload = client.post(
        "/etl/importar-csv",
        files={"file": ("vendas.csv", io.BytesIO(csv_data.encode()), "text/csv")}
    )

    print("Resposta upload:", response_upload.status_code, response_upload.text)
    assert response_upload.status_code == 200
    assert response_upload.json() == {"msg": "Importado com sucesso"}

    # 2. Consulta o relatório do mês
    response_relatorio = client.get("/etl/relatorio-mensal", params={"mes": "2025-07"})
    print("Resposta relatório:", response_relatorio.status_code, response_relatorio.text)
    assert response_relatorio.status_code == 200

    relatorio = response_relatorio.json()

    # 3. Valida os dados
    assert relatorio["mes"] == "2025-07"
    assert relatorio["total_vendas"] == 1200.0  # 200*2 + 300*1 + 100*5
    assert relatorio["total_itens"] == 8        # 2 + 1 + 5
    assert relatorio["vendas_por_categoria"] == {
        "Eletrônicos": 700.0,   # 400 + 300
        "Brinquedos": 500.0     # 100 * 5
    }
    assert relatorio["top_vendedor"] == "Ana"   # Ana: 200*2 + 100*5 = 900
