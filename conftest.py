import pytest
from app.database import Base, engine

@pytest.fixture(autouse=True)
def limpar_banco():
    """
    Fixture executada automaticamente antes e depois de cada teste.
    Ela limpa todas as tabelas do banco de dados (sem apagar a estrutura).
    """
    # 🔄 Antes do teste: limpa todas as tabelas
    conn = engine.connect()
    trans = conn.begin()
    for table in reversed(Base.metadata.sorted_tables):
        conn.execute(table.delete())
    trans.commit()
    conn.close()

    yield  # ⏱ Executa o teste neste ponto

    # 🧹 Depois do teste: (opcional) use aqui se quiser limpar algo mais
    # Exemplo: arquivos, cache, sessões ou mesmo log
