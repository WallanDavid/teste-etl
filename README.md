# 🧪 Projeto ETL com FastAPI, SQLAlchemy e Pandas

Este projeto é um sistema de ETL completo que permite importar vendas via CSV, realizar operações CRUD e gerar relatórios mensais com agregações. Tudo isso usando FastAPI, SQLAlchemy, Pandas e PostgreSQL.

---

## 🚀 Tecnologias

- **FastAPI** — Framework moderno para APIs
- **SQLAlchemy** — ORM para manipulação do banco
- **Pandas** — Transformação e análise de dados
- **PostgreSQL** — Banco de dados relacional
- **Docker** — Containerização
- **Pytest** — Testes automatizados

---

## 📁 Estrutura do Projeto

```
projeto/
├── app/
│   ├── main.py             # Entrypoint da aplicação
│   ├── database.py         # Conexão com o banco
│   ├── models.py           # Modelos do banco
│   ├── schemas.py          # Schemas Pydantic
│   ├── crud.py             # Operações CRUD
│   ├── etl.py              # Lógica ETL
│   └── routers/
│       ├── vendas.py       # Rotas de vendas
│       └── etl.py          # Rotas de ETL
├── tests/                  # Testes automatizados
├── scripts/                # Scripts auxiliares
│   └── populate_db.py      # Popula o banco com dados fake
├── data/
│   └── vendas_exemplo.csv  # CSV de exemplo
├── test_runner.py          # Testes manuais
├── .env                    # Variáveis de ambiente
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Como rodar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/WallanDavid/teste-etl.git
cd teste-etl
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Criar o arquivo `.env`

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
```

> Se estiver usando Docker, esse é o padrão do `docker-compose.yml`.

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Subir o banco com Docker (opcional)

```bash
docker-compose up -d
```

### 6. Rodar o servidor

```bash
uvicorn app.main:app --reload
```

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📬 Endpoints principais

### ➕ Criar venda

```http
POST /vendas
```

```json
{
  "produto": "Notebook",
  "categoria": "Eletrônicos",
  "preco": 2500.00,
  "quantidade": 1,
  "data_venda": "2024-01-15",
  "vendedor": "João",
  "regiao": "Sudeste"
}
```

---

### 📥 Importar CSV

```http
POST /etl/importar-csv
```

- Formato aceito: `multipart/form-data`
- Campos obrigatórios: 
  - `produto`, `categoria`, `preco`, `quantidade`, `data_venda`, `vendedor`, `regiao`

---

### 📊 Relatório mensal

```http
GET /etl/relatorio-mensal?mes=2024-01
```

```json
{
  "mes": "2024-01",
  "total_vendas": 500,
  "vendas_por_categoria": {
    "Eletrônicos": 300,
    "Roupas": 200
  },
  "faturamento_total": 125000.0,
  "ticket_medio": 250.0
}
```

---

## 🧪 Testes

Certifique-se que o servidor esteja rodando (`uvicorn app.main:app --reload`).

### Executar os testes:

```bash
pytest
```

Ou usar o script runner manual:

```bash
python test_runner.py
```

---

## 🐳 Docker

### Subir tudo com Docker:

```bash
docker-compose up --build
```

---

## ✅ Checklist

- [x] CRUD de vendas
- [x] Upload e processamento de CSV
- [x] Relatório mensal com Pandas
- [x] Testes com Pytest
- [x] Dockerfile e docker-compose
- [x] `.gitignore` bem configurado
- [x] Script de carga fake com Faker

---

## 🔥 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.env
.venv/

# IDEs
.vscode/
.idea/

# pandas output
data/export.csv

# Logs
*.log
```

---

## 👨‍💻 Autor

[Wallan David](https://github.com/WallanDavid)

---

## 📄 Licença

MIT © 2025
