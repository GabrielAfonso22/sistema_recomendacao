# 👠 Motor de Recomendação Inteligente | Sonho dos Pés (CRM)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

> **Trabalho de Conclusão de Curso (TCC)** focado no desenvolvimento de um sistema de recomendação de produtos (Cross-Selling) voltado para o varejo de calçados masculinos e femininos, utilizando mineração de dados avançada e regras de associação.

🔗 **Acesso ao Projeto em Produção:** [Clique aqui para acessar o Motor na Nuvem](https://sistema-recomendacao-il5v.onrender.com)

---

## 🎯 Contexto e Desafio de Negócio
No varejo de moda e calçados, um dos maiores desafios para aumentar a rentabilidade é a elevação do **Ticket Médio** (gasto por cliente) e do indicador de **PA (Peças por Atendimento)**. 

Este projeto foi desenhado para resolver essa dor no ecossistema da **Sonho dos Pés**. O sistema atua como uma ferramenta de CRM Inteligente para o time de marketing e gerentes de loja. Em vez de disparar ofertas genéricas, a plataforma analisa o histórico real de milhares de cupons fiscais para identificar quais calçados e acessórios possuem sinergia matemática, permitindo ações de marketing hiper-personalizadas de alta conversão.

---

## 🧠 Arquitetura do Motor e Algoritmos

O coração do sistema é composto por uma abordagem híbrida de inteligência de dados, dividida em duas camadas de segurança para garantir que o usuário nunca fique sem uma recomendação:

### 1. Algoritmo Principal: FP-Growth (Frequent Pattern Growth)
Diferente do algoritmo Apriori tradicional (que é lento e consome muita memória), o **FP-Growth** comprime a base de dados de vendas em uma estrutura de árvore (*FP-Tree*). Ele extrai regras de associação robustas avaliando quatro métricas fundamentais de varejo:
* **Suporte:** A popularidade combinada dos produtos na base de dados global.
* **Confiança:** A certeza de que, ao olhar o Produto A, o cliente também levará o Produto B.
* **Lift:** O fator de relevância. Um Lift maior que 1 indica que a presença do calçado alvo aumenta significativamente a chance de compra do item recomendado.
* **Convicção:** O grau de dependência da regra, medindo o impacto caso a associação estivesse errada.

### 2. Algoritmo de Fallback: Matriz de Coocorrência por Cesta
Para produtos novos ou coleções recentes que ainda não possuem suporte estatístico suficiente para entrar nas regras estritas do FP-Growth, o motor ativa um fallback automático. Ele mapeia em tempo real a interseção de **Basket IDs** (Identificadores de Cesta de Compras), garantindo que os itens mais frequentemente comprados juntos na mesma filial e data sejam sugeridos de forma instantânea.

---

## ✨ Funcionalidades da Plataforma

* **Painel de Alta Conversão (Top Sellers):** Exibe dinamicamente os 20 calçados mais vendidos de toda a rede baseando-se no volume de tickets únicos, permitindo identificar tendências de moda de forma visual.
* **Busca por Referência/SKU:** Consulta rápida que retorna o perfil do produto alvo e um carrossel com até 10 recomendações preditivas completas (com foto garantida, preço, cor e métricas do algoritmo).
* **Simulador de Campanhas Omnichannel:** Permite que o gestor clique em um botão para simular o disparo de uma campanha de e-mail marketing segmentada apenas para as clientes com real potencial de compra daqueles itens complementares.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3 e FastAPI (Framework de altíssimo desempenho para APIs REST).
* **Processamento de Dados:** Pandas e NumPy (Tratamento, saneamento de tipos e padronização de SKUs).
* **Mineração de Dados:** `mlxtend.frequent_patterns` para modelagem do FP-Growth.
* **Frontend:** Interface SPA (Single Page Application) responsiva, limpa e moderna construída com HTML5, CSS3 e JavaScript assíncrono (Fetch API).

---

## 🚀 Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone [https://github.com/GabrielAfonso22/sistema_recomendacao.git](https://github.com/GabrielAfonso22/sistema_recomendacao.git)
cd sistema_recomendacao


## 📺 Demonstração do Sistema em Vídeo

Clique na imagem abaixo para assistir à demonstração completa do motor de recomendação em funcionamento. O vídeo cobre desde a tela de autenticação segura até o processamento do algoritmo FP-Growth em milissegundos, culminando no disparo real da campanha de CRM:

[![Assista à Demonstração do Sistema](https://img.youtube.com/vi/PHAaktW8hJ8/0.jpg)](https://www.youtube.com/watch?v=PHAaktW8hJ8)

*Nota: O vídeo abrirá diretamente em uma nova aba do seu navegador no YouTube.*
