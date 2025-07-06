import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faker import Faker
import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app import crud

fake = Faker("pt_BR")
db = SessionLocal()

produtos = [
    "Notebook", "Mouse", "Teclado", "Monitor", "Impressora",
    "Camisa", "Calça", "Tênis", "Jaqueta", "Relógio",
    "Sofá", "Mesa", "Cadeira", "Cortina", "Luminária",
    "Bola", "Bicicleta", "Raquete", "Esteira", "Skate"
]

categorias = ["Eletrônicos", "Roupas", "Casa", "Esportes", "Livros"]
vendedores = [fake.name() for _ in range(10)]
regioes = ["Norte", "Sul", "Sudeste", "Centro-Oeste", "Nordeste"]  # Corrigido

def gerar_data_venda():
    hoje = datetime.now()
    dias = random.randint(0, 180)
    return hoje - timedelta(days=dias)

for _ in range(500):
    produto = random.choice(produtos)
    categoria = random.choice(categorias)
    preco = round(random.uniform(10.0, 5000.0), 2)
    quantidade = random.randint(1, 10)
    data_venda = gerar_data_venda().date()
    vendedor = random.choice(vendedores)
    regiao = random.choice(regioes)

    venda = {
        "produto": produto,
        "categoria": categoria,
        "preco": preco,
        "quantidade": quantidade,
        "data_venda": data_venda.isoformat(),
        "vendedor": vendedor,
        "regiao": regiao
    }

    crud.criar_venda(db, venda)

db.close()
print("✅ 500 vendas inseridas com sucesso!")
