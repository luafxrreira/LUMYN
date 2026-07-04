import os, dotenv, requests, json

dotenv.load_dotenv()
api_key = os.environ.get("API_KEY")

chat_history = []
print("O modelo de IA utilizado é antigo, pode não saber muitas respostas.")
print("Chat iniciado!")

while True:
    print("\n1. Digite 'sair' para encerrar a conversa." \
    "\n2. Digite 'histórico' para visualzar mensagens anteriores")
    query = input("Faça uma pergunta: ").strip()

    if not query:
        continue

    if query.lower() == 'sair': 
        print("Encerrando o chat. Obrigada por utilizar!")
        break    

    if query.lower() in ['histórico', 'historico']:
        if not chat_history:
            print("[Histórico vazio. Inicie uma conversa com o chat.]")
        else:
            print(10*("-"), "HISTÓRICO DA CONVERSA", 10*("-"), "\n")
            for msg in chat_history:
                papel = "você" if msg["role"] == "user" else "IA"
                print(f"{papel}: {msg['content']}")
            print("\n", 10*("-"), "FIM DO HISTÓRICO", 10*("-"))
        continue

    chat_history.append({
        "role":"user",
        "content": query
        })

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization":f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "openrouter/free",
                    "messages": chat_history,
                }
            ),
        )

        if response.status_code == 200:
            dados = response.json()
            ai_response = dados["choices"][0]["message"]["content"]
            print(f"\nResposta do modelo: {ai_response}")

            chat_history.append({
                "role":"assistant", 
                "content":ai_response
            })

        else:
            print(f"\n[ERRO {response.status_code}] Detalhes:")
            print(response.text)
            chat_history.pop()

    except requests.exceptions.RequestException as e:   
        print(f"erro de conexão: {e}")
        if chat_history:
            chat_history.pop()