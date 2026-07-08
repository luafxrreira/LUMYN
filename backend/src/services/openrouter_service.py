import os, dotenv, json, requests
from src.config.config import get_api_key
from dotenv import load_dotenv

load_dotenv()

def send_message_api_logic(chat_history):
    api_key = get_api_key()

    if not api_key:
        api_key = os.getenv("API_KEY")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization":f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_instruction = {
        "role": "system",
        "content": "Você é o Lumyn, uma inteligência artificial prestativa, inteligente e amigável. Nunca diga que é o ChatGPT, OpenAI ou um modelo genérico. Seu nome é estritamente Lumyn."
    }

    full_messages = [system_instruction] + chat_history

    payload = {
        "model": "openrouter/free",
        "messages": full_messages
        }

    try:
        response = requests.post(
            url, 
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            dados = response.json()
            if "choices" in dados and len(dados["choices"]) > 0:
                return dados["choices"][0]["message"]["content"]

        else:
            print(f"\n(API) {response.status_code}, {response.text}:")
            return None

    except requests.exceptions.RequestException as e:   
        print(f"(API) Não foi possível conectar com a API: {e}")
        return None