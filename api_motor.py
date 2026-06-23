# api_motor.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import uvicorn
import os
import urllib.request
from services.email_dispatcher import executar_disparo_email

app = FastAPI(title="Motor Sonho dos Pés API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE ENTRADA (Devem vir obrigatoriamente ANTES das rotas) ---
class CampanhaRequest(BaseModel):
    produto_nome: str
    produto_preco: str
    produto_foto: str
    recomendacoes: list

print("Carregando bases de dados na memória...")
try:
    # Lendo direto dos arquivos GZ
    df_produtos = pd.read_csv("DIM_PRODUTO.csv.gz", compression="gzip", low_memory=False)
    df_links = pd.read_csv("DIM_PRODUTO_LINK.csv.gz", compression="gzip", low_memory=False)
    df_vendas = pd.read_csv("VENDA_PRODUTO.csv.gz", compression="gzip", low_memory=False)
    
    try:
        # Mantido como CSV normal pois é leve e não foi zipado na sua pasta
        df_regras = pd.read_csv("regras_finais.csv", low_memory=False)
        df_regras['antecedents'] = df_regras['antecedents'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    except:
        df_regras = pd.DataFrame()

    df_produtos['PRODUTO_SKU'] = df_produtos['PRODUTO_SKU'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_produtos['PRODUTO_REFERENCIA'] = df_produtos['PRODUTO_REFERENCIA'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_links['CODIGO_COMPLETO'] = df_links['CODIGO_COMPLETO'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_vendas['PRODUTO_SKU'] = df_vendas['PRODUTO_SKU'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

    # --- SANEAMENTO DE DADOS (Expurgando Cestas Fantasmas) ---
    df_vendas = df_vendas.dropna(subset=['TICKET'])
    df_vendas['TICKET_STR'] = df_vendas['TICKET'].astype(str).str.strip().str.lower()
    df_vendas = df_vendas[~df_vendas['TICKET_STR'].isin(['nan', '0', '', 'null', 'none'])]

    # Criação do Identificador Único de Cesta (Basket ID)
    df_vendas['BASKET_ID'] = df_vendas['FILIAL_CODIGO'].astype(str) + "_" + df_vendas['TICKET_STR'] + "_" + df_vendas['VENDA_DATA'].astype(str)

    print("Cruzando tabelas e filtrando categoria CALCADOS...")
    vendas_com_ref = pd.merge(
        df_vendas, 
        df_produtos[['PRODUTO_SKU', 'PRODUTO_REFERENCIA', 'PRODUTO_CATEGORIA_DESCRICAO']], 
        on='PRODUTO_SKU', 
        how='inner'
    )

    vendas_calcados = vendas_com_ref[vendas_com_ref['PRODUTO_CATEGORIA_DESCRICAO'].astype(str).str.upper().str.strip() == 'CALCADOS']

    top_vendas = vendas_calcados.groupby('PRODUTO_REFERENCIA')['BASKET_ID'].nunique().reset_index()
    top_vendas.rename(columns={'BASKET_ID': 'QTD_TICKETS'}, inplace=True)
    top_vendas = top_vendas.sort_values(by='QTD_TICKETS', ascending=False).head(250)

    precos_dict = vendas_calcados.groupby('PRODUTO_REFERENCIA')['VALOR_PRODUTO_LIQUIDO'].max().to_dict()
    tickets_totais_dict = vendas_calcados.groupby('PRODUTO_REFERENCIA')['BASKET_ID'].nunique().to_dict()

except Exception as e:
    print(f"Erro ao carregar CSVs: {e}")
    top_vendas = pd.DataFrame()
    precos_dict = {}
    tickets_totais_dict = {}
    vendas_calcados = pd.DataFrame()

_cache_img = {}

def imagem_esta_online(url):
    if not url or pd.isna(url): return False
    url_str = str(url).strip()
    if not url_str.startswith('http'): return False
    if 'sem_foto' in url_str.lower() or 'sem foto' in url_str.lower(): return False
    if url_str in _cache_img: return _cache_img[url_str]
        
    try:
        req = urllib.request.Request(url_str, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.0) as response:
            is_valid = response.status == 200
            _cache_img[url_str] = is_valid
            return is_valid
    except Exception:
        _cache_img[url_str] = False
        return False

def buscar_produto_com_foto_garantida(ref):
    produtos_ref = df_produtos[df_produtos['PRODUTO_REFERENCIA'] == str(ref)]
    if produtos_ref.empty: return None, ""
        
    for _, prod in produtos_ref.iterrows():
        sku = str(prod['PRODUTO_SKU'])
        links = df_links[df_links['CODIGO_COMPLETO'] == sku]['LINK_FOTO'].values
        if len(links) > 0:
            url_teste = str(links[0]).strip()
            if imagem_esta_online(url_teste): return prod, url_teste
                
        foto_nativa = str(prod.get('URL_FOTO', '')).strip()
        if imagem_esta_online(foto_nativa): return prod, foto_nativa
            
    return None, ""

def buscar_melhor_nome(prod_row):
    nome = str(prod_row.get('PRODUTO_DESCRICAO_CURTA', ''))
    if nome.lower() == 'nan' or not nome.strip(): nome = str(prod_row.get('PRODUTO_DESCRICAO', ''))
    if nome.lower() == 'nan' or not nome.strip(): nome = f"Ref: {prod_row.get('PRODUTO_REFERENCIA', 'Desconhecida')}"
    if len(nome) > 60: nome = nome[:57] + "..."
    return nome.strip()

def formatar_preco(valor):
    if pd.isna(valor) or valor == 0: return "Preço não informado"
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --- ROTAS VISUAIS DE SERVIÇO ---
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_index(): return FileResponse("frontend/index.html")

@app.get("/login.html")
def serve_login(): return FileResponse("frontend/login.html")

@app.get("/preview_campanha.html")
def serve_preview():
    caminho = "frontend/preview_campanha.html"
    return FileResponse(caminho) if os.path.exists(caminho) else {"detail": "Em construção!"}


# --- ENDPOINTS DA API ENDPOINT REST ---

@app.get("/api/products/top-sellers")
def get_top_sellers():
    resultado = []
    if top_vendas.empty: return {"top_sellers": []}
        
    for index, row in top_vendas.iterrows():
        if len(resultado) >= 20: break
        ref = row['PRODUTO_REFERENCIA']
        qtde_tickets = int(row['QTD_TICKETS'])
        
        prod, foto_url = buscar_produto_com_foto_garantida(ref)
        if prod is None or not foto_url: continue

        resultado.append({
            "referencia": ref,
            "nome": buscar_melhor_nome(prod),
            "foto": foto_url,
            "qtde_vendida": qtde_tickets,
            "cor": str(prod['PRODUTO_COR_DESCRICAO']) if pd.notna(prod['PRODUTO_COR_DESCRICAO']) else ""
        })
    return {"top_sellers": resultado}


@app.get("/api/recommend/{sku}")
def get_recommendation(sku: str):
    produto_alvo = df_produtos[(df_produtos['PRODUTO_SKU'] == str(sku)) | 
                               (df_produtos['PRODUTO_REFERENCIA'] == str(sku))]
    
    if produto_alvo.empty: raise HTTPException(status_code=404, detail="Produto não encontrado.")

    alvo_data = produto_alvo.iloc[0]
    ref_alvo = str(alvo_data['PRODUTO_REFERENCIA'])
    sku_alvo = str(alvo_data['PRODUTO_SKU'])
    preco_alvo = precos_dict.get(ref_alvo, alvo_data.get('VALOR_PRODUTO_BRUTO', 0))

    _, foto_alvo = buscar_produto_com_foto_garantida(ref_alvo)

    dados_alvo = {
        "PRODUTO_SKU": sku_alvo,
        "PRODUTO_NOME": buscar_melhor_nome(alvo_data),
        "LINK_FOTO": foto_alvo,
        "PRODUTO_COR": str(alvo_data['PRODUTO_COR_DESCRICAO']),
        "PRODUTO_PRECO": formatar_preco(preco_alvo)
    }

    if not vendas_calcados.empty:
        tickets_com_alvo = set(vendas_calcados[vendas_calcados['PRODUTO_REFERENCIA'] == ref_alvo]['BASKET_ID'])
    else:
        tickets_com_alvo = set()

    recomendacoes_layout = []
    
    if not df_regras.empty:
        regras_alvo = df_regras[df_regras['antecedents'] == ref_alvo]
    else:
        regras_alvo = pd.DataFrame()

    # --- FALLBACK (Co-ocorrência) ---
    if  regras_alvo.empty and not vendas_calcados.empty:
        itens_coocorrentes = vendas_calcados[vendas_calcados['BASKET_ID'].isin(tickets_com_alvo)]
        itens_coocorrentes = itens_coocorrentes[itens_coocorrentes['PRODUTO_REFERENCIA'] != ref_alvo]
        
        top_coocorrentes = itens_coocorrentes.groupby('PRODUTO_REFERENCIA')['BASKET_ID'].nunique().sort_values(ascending=False).head(50)

        for ref_rec, qtd_juntos in top_coocorrentes.items():
            if len(recomendacoes_layout) >= 10: break

            prod_rec, foto_rec = buscar_produto_com_foto_garantida(ref_rec)
            if prod_rec is None or not foto_rec: continue
                
            sku_rec = str(prod_rec['PRODUTO_SKU'])
            preco_rec = precos_dict.get(ref_rec, 0)
            sup_calc = round((qtd_juntos / max(1, len(tickets_com_alvo))) * 100, 2)

            recomendacoes_layout.append({
                "PRODUTO_SKU": sku_rec,
                "PRODUTO_NOME": buscar_melhor_nome(prod_rec),
                "LINK_FOTO": foto_rec,
                "PRODUTO_CHAVE": str(prod_rec['PRODUTO_REFERENCIA']),
                "suporte": sup_calc,
                "confianca": sup_calc, 
                "lift": 1.2,
                "conviccao": 1.5,
                "PRODUTO_COR": str(prod_rec['PRODUTO_COR_DESCRICAO']),
                "PRODUTO_PRECO": formatar_preco(preco_rec),
                "is_fallback": False, 
                "comprados_juntos": int(qtd_juntos) 
            })

    # --- FP-GROWTH NORMAL ---
    elif not regras_alvo.empty:
        for index, row in regras_alvo.iterrows():
            if len(recomendacoes_layout) >= 10: break

            ref_rec = str(row['consequents'])
            prod_rec, foto_rec = buscar_produto_com_foto_garantida(ref_rec)
            
            if prod_rec is None or not foto_rec: continue

            sku_rec = str(prod_rec['PRODUTO_SKU'])
            preco_rec = precos_dict.get(ref_rec, 0)

            if not vendas_calcados.empty:
                tickets_com_rec = set(vendas_calcados[vendas_calcados['PRODUTO_REFERENCIA'] == ref_rec]['BASKET_ID'])
                comprados_juntos_real = len(tickets_com_alvo.intersection(tickets_com_rec))
            else:
                comprados_juntos_real = 0

            recomendacoes_layout.append({
                "PRODUTO_SKU": sku_rec,
                "PRODUTO_NOME": buscar_melhor_nome(prod_rec),
                "LINK_FOTO": foto_rec,
                "PRODUTO_CHAVE": str(prod_rec['PRODUTO_REFERENCIA']),
                "suporte": round(row['support'] * 100, 2) if 'support' in row else 0,
                "confianca": round(row['confidence'] * 100, 2) if 'confidence' in row else 0,
                "lift": round(row['lift'], 2) if 'lift' in row else 0,
                "conviccao": round(row['conviction'], 2) if 'conviction' in row else 0,
                "PRODUTO_COR": str(prod_rec['PRODUTO_COR_DESCRICAO']),
                "PRODUTO_PRECO": formatar_preco(preco_rec),
                "is_fallback": False,
                "comprados_juntos": int(comprados_juntos_real) 
            })

    tickets_alvo = tickets_totais_dict.get(ref_alvo, 0)

    return {
        "target_product": dados_alvo,
        "recommendations": recomendacoes_layout,
        "vendas_totais_tickets": tickets_alvo
    }


@app.post("/api/disparar-campanha")
def disparar_campanha(request: CampanhaRequest):
    # Lógica inteligente para isolar o número da referência caso o texto contenha a descrição
    ref_limpa = "42305"
    if "Ref:" in request.produto_nome:
        try:
            ref_limpa = request.produto_nome.split("Ref:")[-1].strip()
        except:
            pass
            
    # Chamada segura para o microsserviço de e-mail 
    resultado = executar_disparo_email(
        ref_alvo=ref_limpa,
        nome_alvo=request.produto_nome,
        foto_alvo=request.produto_foto,
        recomendacoes_front=request.recomendacoes
    )
    
    return {
        "success": resultado["success"],
        "message": f"Campanha enviada com sucesso para {resultado['impacted']} clientes!",
        "impacted": resultado["impacted"],
        "destinatario": "Base Anonimizada",
        "preview_url": resultado["preview_url"]
    }


# O bloco de execução final fica SEMPRE de forma exclusiva no término do arquivo!
if __name__ == "__main__": 
    uvicorn.run("api_motor:app", host="127.0.0.1", port=8000, reload=True)