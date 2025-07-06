import requests
import pandas as pd
import time

BASE_URL = "http://localhost:8000"

def test_basic_crud():
    """Testa operações básicas de criação, listagem e busca de venda"""
    venda_data = {
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "preco": 2500.00,
        "quantidade": 1,
        "data_venda": "2024-01-15",
        "vendedor": "João",
        "regiao": "Sudeste"
    }

    # Criar venda
    response = requests.post(f"{BASE_URL}/vendas", json=venda_data)
    assert response.status_code == 201, f"Erro ao criar venda: {response.text}"
    venda_id = response.json().get("id")
    assert venda_id, "Resposta não contém ID"

    # Buscar por ID
    response = requests.get(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 200, "Erro ao buscar venda por ID"

    # Listar todas
    response = requests.get(f"{BASE_URL}/vendas")
    assert response.status_code == 200, "Erro ao listar vendas"

    print("✅ CRUD básico funcionando")


def test_etl_csv():
    """Testa importação via CSV usando pandas"""
    df = pd.DataFrame({
        'produto': ['Mouse', 'Teclado'],
        'categoria': ['Eletrônicos', 'Eletrônicos'],
        'preco': [50.0, 150.0],
        'quantidade': [2, 1],
        'data_venda': ['2024-01-10', '2024-01-11'],
        'vendedor': ['Maria', 'José'],
        'regiao': ['Sul', 'Norte']
    })

    csv_content = df.to_csv(index=False)
    files = {'file': ('teste.csv', csv_content, 'text/csv')}
    response = requests.post(f"{BASE_URL}/etl/importar-csv", files=files)

    assert response.status_code == 200, f"Erro na importação CSV: {response.text}"
    print("✅ Importação CSV funcionando")


def test_relatorio():
    """Testa geração de relatório mensal"""
    response = requests.get(f"{BASE_URL}/etl/relatorio-mensal?mes=2024-01")
    assert response.status_code == 200, "Erro ao gerar relatório mensal"

    data = response.json()
    assert "total_vendas" in data, "total_vendas ausente no relatório"
    assert "vendas_por_categoria" in data, "vendas_por_categoria ausente no relatório"
    assert "top_vendedor" in data, "top_vendedor ausente no relatório"

    print("✅ Relatório mensal funcionando")


def run_all_tests():
    print("🚀 Iniciando testes...")
    time.sleep(3)  # Tempo para garantir que o servidor subiu
    try:
        test_basic_crud()
        test_etl_csv()
        test_relatorio()
        print("\n🎉 Todos os testes passaram com sucesso!")
    except Exception as e:
        print(f"\n❌ Teste falhou: {e}")


if __name__ == "__main__":
    run_all_tests()
