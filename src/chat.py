from search import search_prompt


def main():
    print("Chat RAG iniciado. Digite sua pergunta ou '/sair' para encerrar.")

    while True:
        question = input("\nVoce: ").strip()

        if question.lower() in {"/sair", "sair", "exit", "quit"}:
            print("Encerrando chat.")
            break

        if not question:
            print("Assistente: Digite uma pergunta valida.")
            continue

        try:
            answer = search_prompt(question)
            print(f"Assistente: {answer}")
        except Exception as exc:
            print(f"Assistente: Erro ao processar pergunta: {exc}")


if __name__ == "__main__":
    main()