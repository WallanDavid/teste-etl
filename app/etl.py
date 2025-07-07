import pandas as pd
import io
from datetime import datetime

def processar_csv(arquivo_csv: bytes):
    """
    Processa um CSV em memória, sanitiza os dados e retorna um DataFrame limpo.
    """
    df = pd.read_csv(io.StringIO(arquivo_csv.decode('utf-8')))

    # Limpeza básica
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Conversões de tipo
    df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')

    # Filtros de integridade
    df = df[(df['preco'] > 0) & (df['quantidade'] > 0)]
    df = df[df['data_venda'] <= datetime.now()]

    return df


def gerar_relatorio_mensal(df: pd.DataFrame, mes: str):
    """
    Gera um dicionário com resumo mensal de vendas.
    """
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df['mes'] = df['data_venda'].dt.to_period("M").astype(str)
    df_mes = df[df['mes'] == mes]

    if df_mes.empty:
        return {
            "mes": mes,
            "total_vendas": 0.0,
            "total_itens": 0,
            "vendas_por_categoria": {},
            "top_vendedor": None
        }

    total_vendas = (df_mes['preco'] * df_mes['quantidade']).sum()
    total_itens = df_mes['quantidade'].sum()

    # Vendas por categoria
    vendas_categoria = (
        df_mes
        .groupby('categoria', group_keys=False)
        .apply(lambda x: (x['preco'] * x['quantidade']).sum())
        .to_dict()
    )

    # Top vendedor com segurança
    vendas_por_vendedor = (
        df_mes
        .groupby('vendedor', group_keys=False)
        .apply(lambda x: (x['preco'] * x['quantidade']).sum())
    )

    top_vendedor = None
    if not vendas_por_vendedor.empty:
        vendas_por_vendedor = vendas_por_vendedor.dropna().astype(float)
        if not vendas_por_vendedor.empty:
            top_vendedor = vendas_por_vendedor.idxmax()

    return {
        "mes": mes,
        "total_vendas": float(total_vendas),
        "total_itens": int(total_itens),
        "vendas_por_categoria": vendas_categoria,
        "top_vendedor": top_vendedor
    }
