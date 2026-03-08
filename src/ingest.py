import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "pdf/examen.pdf")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/rag"
)
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_chunks")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def ingest_pdf():
    pdf_file = Path(PDF_PATH)

    if not pdf_file.exists():
        raise FileNotFoundError(f"Arquivo PDF nao encontrado em: {pdf_file}")

    loader = PyPDFLoader(str(pdf_file))
    documents = loader.load()

    if not documents:
        raise ValueError("Nenhum conteudo foi extraido do PDF informado.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index
        chunk.metadata["source_file"] = str(pdf_file)

    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    ids = [str(uuid4()) for _ in chunks]
    vector_store.add_documents(documents=chunks, ids=ids)

    print(
        f"Ingestao concluida: {len(documents)} paginas, {len(chunks)} chunks salvos em '{PG_VECTOR_COLLECTION_NAME}'."
    )


if __name__ == "__main__":
    ingest_pdf()