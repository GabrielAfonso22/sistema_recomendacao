# 👠 Motor de Recomendação Inteligente | Sonho dos Pés (CRM)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

> **Trabalho de Conclusão de Curso (TCC)** focado no desenvolvimento de um sistema de recomendação de produtos (Cross-Selling) voltado para o varejo de calçados, utilizando regras de associação e mineração de dados.

🔗 **Acesso ao Projeto em Produção:** [Clique aqui para acessar o Motor na Nuvem](https://sistema-recomendacao-il5v.onrender.com)

---

## 🎯 Sobre o Projeto
O sistema processa milhares de tickets de vendas reais para descobrir padrões de compras dos consumidores. Quando um vendedor ou gestor pesquisa por um calçado, a API retorna instantaneamente quais outros produtos têm a maior probabilidade de serem comprados juntos, otimizando o envio de campanhas de e-mail marketing.

## ✨ Funcionalidades
- **Recomendação Principal (FP-Growth):** Sugestões baseadas em Regras de Associação com cálculo de suporte, confiança, lift e convicção.
- **Fallback Inteligente (Coocorrência):** Algoritmo secundário que assume o controle caso o produto não tenha regras formais no FP-Growth.
- **Ranking em Tempo Real:** Painel lateral gerado dinamicamente com os "Top 20 Mais Vendidos".
- **Geração de Campanhas:** Disparo simulado de e-mail marketing automatizado para bases de clientes segmentadas.
- **Frontend Integrado:** Interface gráfica moderna e responsiva construída em HTML/CSS/JS e servida estaticamente via FastAPI.

---

## 🧠 Engenharia de Dados & Otimização de Nuvem
Para permitir que o projeto rodasse no plano gratuito do **Render (limite de 512 MB de RAM)**, foi implementada uma etapa rigorosa de pré-processamento. 
O script `preparar_dados_nuvem.py` filtra a categoria "CALCADOS", cria chaves de agrupamento (Basket IDs) e exporta versões ultra-leves das bases de dados em formato `.csv.gz`. Isso reduziu o consumo de memória da API para menos de **80 MB em tempo real**.

---

## 🛠️ Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone [https://github.com/GabrielAfonso22/sistema_recomendacao.git](https://github.com/GabrielAfonso22/sistema_recomendacao.git)
cd sistema_recomendacao
