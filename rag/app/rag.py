import os
import re
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable

load_dotenv()

DB_URL         = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]   = os.getenv("LANGSMITH_PROJECT", "desafio")

_custom_prompt = PromptTemplate(
    input_variables=["input", "table_info"],
    template="""
Você é um agente SQL especializado em PostgreSQL. Sua única tarefa é gerar consultas SQL válidas.

REGRAS ESTRITAS:
1. NUNCA use blocos de markdown (```sql ou ```)
2. Use SOMENTE funções PostgreSQL: CURRENT_DATE, NOW(), INTERVAL, DATE_TRUNC, EXTRACT
3. Formate datas com 'YYYY-MM-DD'
4. Retorne APENAS o código SQL puro, sem comentários ou explicações

Estrutura do banco:
{table_info}

Pergunta:
{input}

SQL:
""".strip(),
)


answer_prompt = ChatPromptTemplate.from_template("""
Você é um analista de dados. Responda em português, de forma clara e direta:

Pergunta: {question}
Dados: {query_result}

Resposta (sem termos técnicos):
""")

def clean_sql(sql: str) -> str:
 
    cleaned = re.sub(r'```sql|```', '', sql, flags=re.IGNORECASE)
    
    cleaned = re.sub(r'^\s*(CREATE|DROP|ALTER|INSERT|UPDATE|DELETE).*', '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
    
    cleaned = re.sub(r'--.*$', '', cleaned, flags=re.MULTILINE)
    
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

@traceable(name="SalesInsightRAG")
def run_rag_query(question: str) -> str:

    if not GEMINI_API_KEY or not DB_URL:
        raise EnvironmentError("As variáveis de ambiente GEMINI_API_KEY ou DB_URL não estão definidas.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0,
    )
    db = SQLDatabase.from_uri(DB_URL)

    generate_query_chain = (
        _custom_prompt
        | llm
        | StrOutputParser()
    )

    answer_generation_chain = (
        answer_prompt
        | llm
        | StrOutputParser()
    )

    table_info = db.get_table_info()

    sql_query_raw = generate_query_chain.invoke({
        "input": question,
        "table_info": table_info
    })

    sql_query_cleaned = clean_sql(sql_query_raw)
    
    if not sql_query_cleaned:
        return "Não foi possível gerar uma consulta SQL válida para a sua pergunta."


    try:
        query_result = db.run(sql_query_cleaned)
    except Exception as e:
    
        print(f"Erro ao executar SQL: {e}")
        return "Ocorreu um erro ao consultar o banco de dados. A consulta gerada pode ser inválida."


    final_answer = answer_generation_chain.invoke({
        "question": question,
        "query_result": query_result,
    })

    return final_answer