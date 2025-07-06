import pandas as pd
import io
from datetime import datetime

def processar_csv(arquivo_csv: bytes):
    df = pd.read_csv(io.StringIO(arquivo_csv.decode('utf-8')))
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')

    df = df[(df['preco'] > 0) & (df['quantidade'] > 0)]
    df = df[df['data_venda'] <= datetime.now()]
    return df

def gerar_relatorio_mensal(df: pd.DataFrame, mes: str):
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    df['mes'] = df['data_venda'].dt.to_period("M").astype(str)
    df_mes = df[df['mes'] == mes]

    total_vendas = (df_mes['preco'] * df_mes['quantidade']).sum()
    total_itens = df_mes['quantidade'].sum()

    vendas_categoria = (df_mes.groupby('categoria')
                        .apply(lambda x: (x['preco'] * x['quantidade']).sum())
                        .to_dict())

    top_vendedor = (df_mes.groupby('vendedor')
                    .apply(lambda x: (x['preco'] * x['quantidade']).sum())
                    .idxmax())

    return {
        "mes": mes,
        "total_vendas": float(total_vendas),
        "total_itens": int(total_itens),
        "vendas_por_categoria": vendas_categoria,
        "top_vendedor": top_vendedor
    }
