# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um fluxo simples de RAG com PDF + PostgreSQL/pgVector.

## Fonte de Dados
Nesse projeto foi utilizado um pdf com dados de manutenções elétricas.

Exemplos de pergunta:
 O que é um Relé de gás atuado?
 O que é Sobreaquecimento excessivo nos conectores?
 Quais os benefíciso do da TERMOGRAFIA?

## Configurando ambiente PYTHON

1. Rodar o comando: 
python3 -m venv venv source venv/bin/activate (instale o python antes caso não tenha :P)

2. Instalar as dependências:
pip install -r requirements.txt

3. Duplique o arquivo .env.example e renomeie para .env

## Como executar o projeto

1. Subir o banco PostgreSQL com pgVector rodando o comando abaixo:

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