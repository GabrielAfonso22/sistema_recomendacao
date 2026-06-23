import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

def treinar_motor():
    print("1. Lendo os arquivos CSV direto dos GZs...")
    df_produtos = pd.read_csv("DIM_PRODUTO.csv.gz", compression="gzip")
    df_vendas = pd.read_csv("VENDA_PRODUTO.csv.gz", compression="gzip")

    print("2. Juntando as tabelas e limpando...")
    df_completo = pd.merge(df_vendas, df_produtos[['PRODUTO_SKU', 'PRODUTO_REFERENCIA']], on='PRODUTO_SKU', how='inner')

    print("3. Criando as cestas por TICKET...")
    # Converte para string para garantir que a cesta fique certinha
    df_completo['PRODUTO_REFERENCIA'] = df_completo['PRODUTO_REFERENCIA'].astype(str)
    cestas = df_completo.groupby('TICKET')['PRODUTO_REFERENCIA'].apply(list).tolist()

    if not cestas:
        print("Erro: Nenhuma cesta criada. A base de vendas está vazia ou os SKUs não batem.")
        return

    print("4. Rodando o FP-Growth (Isso pode demorar um pouquinho dependendo do tamanho da base)...")
    te = TransactionEncoder()
    te_ary = te.fit(cestas).transform(cestas)
    df_cestas = pd.DataFrame(te_ary, columns=te.columns_)

    # Reduzi o suporte mínimo pra garantir que acha regras até em bases pequenas (0.001 = 0.1%)
    itens_frequentes = fpgrowth(df_cestas, min_support=0.001, use_colnames=True)

    if itens_frequentes.empty:
        print("Aviso: O suporte mínimo foi muito alto e não achou regras. Verifique a quantidade de dados.")
        return

    # Gera as métricas Confiança, Lift, etc.
    regras = association_rules(itens_frequentes, metric="confidence", min_threshold=0.1)
    
    if regras.empty:
        print("Aviso: Nenhuma regra superou a confiança mínima.")
        return

    # Limpando o formato para salvar no CSV
    regras['antecedents'] = regras['antecedents'].apply(lambda x: list(x)[0])
    regras['consequents'] = regras['consequents'].apply(lambda x: list(x)[0])
    
    # Salva o arquivo final!
    regras.to_csv("regras_finais.csv", index=False)
    print("5. Uhuul! As regras foram geradas e salvas em 'regras_finais.csv'!")

if __name__ == "__main__":
    treinar_motor()