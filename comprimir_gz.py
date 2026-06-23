import pandas as pd

print("Iniciando a compactação profissional (GZIP)...")

print("1/3 - Comprimindo VENDA_PRODUTO...")
df_vendas = pd.read_csv("VENDA_PRODUTO.csv", low_memory=False)
df_vendas.to_csv("VENDA_PRODUTO.csv.gz", compression="gzip", index=False)

print("2/3 - Comprimindo DIM_PRODUTO...")
df_produtos = pd.read_csv("DIM_PRODUTO.csv", low_memory=False)
df_produtos.to_csv("DIM_PRODUTO.csv.gz", compression="gzip", index=False)

print("3/3 - Comprimindo DIM_PRODUTO_LINK...")
df_links = pd.read_csv("DIM_PRODUTO_LINK.csv", low_memory=False)
df_links.to_csv("DIM_PRODUTO_LINK.csv.gz", compression="gzip", index=False)

print("Sucesso! Os arquivos .gz foram criados. Pode apagar os .csv originais gigantes!")