# Sales Insights API - Agente RAG com Gemini

Este projeto foi desenvolvido como parte de um processo seletivo, demonstrando a criação de uma API de análise de vendas que utiliza um agente RAG (Retrieval-Augmented Generation) com o modelo Gemini do Google para responder a perguntas em linguagem natural sobre dados de um banco de dados PostgreSQL.

## 📜 Visão Geral

A aplicação consiste em uma API RESTful construída com FastAPI que expõe endpoints para obter insights de vendas. O principal diferencial é o endpoint `/sales-insights`, que permite ao usuário fazer perguntas complexas em português (ex: "qual foi o produto mais vendido no último mês?"), que são traduzidas para consultas SQL, executadas e respondidas de forma clara e objetiva.

## ✨ Features

-   **API RESTful**: Interface clara e documentada para interagir com os dados de vendas.
-   **Análise de Vendas**: Endpoint `/top-products` para listar os produtos mais vendidos no último mês.
-   **Consultas em Linguagem Natural**: Endpoint `/sales-insights` que utiliza um agente RAG com o LLM Gemini 1.5 Flash para responder perguntas sobre os dados.
-   **Arquitetura Robusta**: Uso de SQLAlchemy para ORM, Pydantic para validação de dados e LangChain para orquestrar a lógica do agente.
-   **Ambiente Containerizado**: Configuração completa com Docker e Docker Compose para garantir uma execução simples e consistente em qualquer ambiente.

## 🛠️ Arquitetura e Tecnologias

O projeto utiliza as seguintes tecnologias:

-   **Backend**: Python 3.9+
-   **Framework da API**: FastAPI
-   **Banco de Dados**: PostgreSQL
-   **ORM**: SQLAlchemy
-   **LLM e RAG**: Google Gemini & LangChain
-   **Containerização**: Docker & Docker Compose

### Fluxo da Requisição RAG (`/sales-insights`)

1.  **Pergunta do Usuário**: O usuário envia uma pergunta em linguagem natural (ex: "Qual cliente comprou mais?").
2.  **Geração de SQL**: O LangChain, com a ajuda do prompt de engenharia e do modelo Gemini, analisa a pergunta e a estrutura das tabelas do banco de dados para gerar uma consulta SQL correspondente.
3.  **Limpeza da Consulta**: Uma função intermediária remove artefatos (como blocos de markdown ` ```sql`) da consulta gerada pelo LLM.
4.  **Execução no BD**: A consulta SQL limpa é executada no banco de dados PostgreSQL.
5.  **Geração da Resposta**: O resultado da consulta é enviado de volta ao Gemini, que gera uma resposta final em português, de forma clara e não-técnica.
6.  **Resposta da API**: A API retorna a resposta final ao usuário.

## 🚀 Como Rodar o Projeto

A maneira mais simples de rodar este projeto é utilizando Docker.

### Pré-requisitos

-   [Docker](https://www.docker.com/get-started) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.
-   Uma chave de API do **Google Gemini**. Você pode obter uma gratuitamente no [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```
### 2. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto, copiando o conteúdo do arquivo de exemplo `.env.example`.

```bash
# .env

# --- API & RAG Configuration ---
# Cole sua chave de API do Gemini aqui
GEMINI_API_KEY="COLE_SUA_CHAVE_AQUI"
LANGSMITH_PROJECT="desafio-sales-insights" # Opcional: Para tracing com LangSmith

# --- Database Configuration (for Docker Compose) ---
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=sales_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# SQLAlchemy Database URL
DATABASE_URL="postgresql://user:password@db:5432/sales_db"
```
### 3. Popular o Banco de Dados com Dados de Exemplo
### 4. Baixe as dependências: pip install -r requirements.txt
### 5. Inicie o ambiente virtual
### 6. Inicie o servidor fastAPI
### 7. Acesse: ➡️ http://localhost:8000/docs
### 8. No endpoint "/sales-insights" teste a IA
