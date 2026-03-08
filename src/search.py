import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DATABASE_URL = os.getenv(
  "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/rag"
)
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_chunks")
K_RESULTS = 10


def _validate_database_url(database_url: str) -> None:
  if database_url.startswith(("http://", "https://")):
    raise ValueError(
      "DATABASE_URL invalido. Use uma URL PostgreSQL, por exemplo: "
      "postgresql+psycopg://postgres:postgres@localhost:5432/rag"
    )


def _build_context(documents) -> str:
  if not documents:
    return ""

  chunks = []
  for index, doc in enumerate(documents, start=1):
    source = doc.metadata.get("source_file", doc.metadata.get("source", "desconhecido"))
    page = doc.metadata.get("page", "N/A")
    text = doc.page_content.strip()
    chunks.append(f"[{index}] source={source} page={page}\n{text}")

  return "\n\n".join(chunks)


def search_prompt(question=None):
  if not question or not question.strip():
    return "Pergunta vazia. Digite uma pergunta valida."

  _validate_database_url(DATABASE_URL)

  embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
  vector_store = PGVector(
    embeddings=embeddings,
    collection_name=PG_VECTOR_COLLECTION_NAME,
    connection=DATABASE_URL,
    use_jsonb=True,
  )

  query_vector = embeddings.embed_query(question)
  documents = vector_store.similarity_search_by_vector(query_vector, k=K_RESULTS)
  contexto = _build_context(documents)

  prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
  llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=0)
  response = llm.invoke(prompt)

  return response.content.strip()