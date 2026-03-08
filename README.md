# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um fluxo simples de RAG com PDF + PostgreSQL/pgVector.
## Como executar

1. Subir o banco PostgreSQL com pgVector

```bash
docker compose up -d
```

2. Executar a ingestao do PDF (quebra em chunks e salva embeddings no banco)

```bash
python src/ingest.py
```

3. Executar o chat no terminal para fazer perguntas ao modelo

```bash
python src/chat.py
```

## Fluxo do projeto

- `src/ingest.py`: le o PDF de `PDF_PATH`, divide em chunks (1000 com overlap 150), gera embeddings e salva no pgVector.
- `src/chat.py`: inicia um chat no terminal.
- `src/search.py`: vetoriza a pergunta, busca os 10 chunks mais relevantes (`k=10`), monta o prompt e chama a LLM.

## Observacoes

- Se estiver usando o ambiente virtual em `source/`, execute com:

```bash
source/Scripts/python.exe src/ingest.py
source/Scripts/python.exe src/chat.py
```

- Para encerrar o chat, digite `/sair`.