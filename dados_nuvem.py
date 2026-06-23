# preparar_dados_nuvem.py
import pandas as pd

print("Iniciando super otimização de dados para o Render Free...")

# 1. Otimizar Produtos
print("1/3 - Filtrando colunas de DIM_PRODUTO...")
cols_prod = ['PRODUTO_SKU', 'PRODUTO_REFERENCIA', 'PRODUTO_CATEGORIA_DESCRICAO', 
             'PRODUTO_COR_DESCRICAO', 'PRODUTO_DESCRICAO_CURTA', 'PRODUTO_DESCRICAO']
df_prod = pd.read_csv("DIM_PRODUTO.csv.gz", compression="gzip", usecols=cols_prod, low_memory=False)

# Padronizar o SKU para Texto (Evita o erro de tipos misturados no merge)
df_prod['PRODUTO_SKU'] = df_prod['PRODUTO_SKU'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

df_prod.to_csv("produtos_nuvem.csv.gz", compression="gzip", index=False)

# 2. Otimizar Links
print("2/3 - Filtrando colunas de DIM_PRODUTO_LINK...")
cols_links = ['CODIGO_COMPLETO', 'LINK_FOTO']
df_links = pd.read_csv("DIM_PRODUTO_LINK.csv.gz", compression="gzip", usecols=cols_links, low_memory=False)
df_links.to_csv("links_nuvem.csv.gz", compression="gzip", index=False)

# 3. Otimizar Vendas
print("3/3 - Processando e encolhendo a base de VENDA_PRODUTO...")
cols_vendas = ['TICKET', 'FILIAL_CODIGO', 'VENDA_DATA', 'PRODUTO_SKU', 'VALOR_PRODUTO_LIQUIDO']
df_vendas = pd.read_csv("VENDA_PRODUTO.csv.gz", compression="gzip", usecols=cols_vendas, low_memory=False)

# Saneamento básico das vendas
df_vendas = df_vendas.dropna(subset=['TICKET'])
df_vendas['TICKET_STR'] = df_vendas['TICKET'].astype(str).str.strip().str.lower()
df_vendas = df_vendas[~df_vendas['TICKET_STR'].isin(['nan', '0', '', 'null', 'none'])]

# Padronizar o SKU para Texto em Vendas também (Garante que os tipos fiquem idênticos para o merge)
df_vendas['PRODUTO_SKU'] = df_vendas['PRODUTO_SKU'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

# Agora o merge vai funcionar perfeitamente!
vendas_com_ref = pd.merge(
    df_vendas, 
    df_prod[['PRODUTO_SKU', 'PRODUTO_REFERENCIA', 'PRODUTO_CATEGORIA_DESCRICAO']], 
    on='PRODUTO_SKU', 
    how='inner'
)
vendas_calcados = vendas_com_ref[vendas_com_ref['PRODUTO_CATEGORIA_DESCRICAO'].astype(str).str.upper().str.strip() == 'CALCADOS'].copy()

# Pré-calcular o Basket ID
vendas_calcados['BASKET_ID'] = vendas_calcados['FILIAL_CODIGO'].astype(str) + "_" + vendas_calcados['TICKET_STR'] + "_" + vendas_calcados['VENDA_DATA'].astype(str)

# Manter apenas o mínimo para a API funcionar
cols_finais_vendas = ['PRODUTO_SKU', 'PRODUTO_REFERENCIA', 'VALOR_PRODUTO_LIQUIDO', 'BASKET_ID']
vendas_calcados = vendas_calcados[cols_finais_vendas]

vendas_calcados.to_csv("vendas_calcados_nuvem.csv.gz", compression="gzip", index=False)

print("\n✔ Sucesso absoluto! Os 3 arquivos '*_nuvem.csv.gz' foram criados e estão super leves!")