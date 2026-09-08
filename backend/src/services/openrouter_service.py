import os, time
from dotenv import load_dotenv  
from langchain_openrouter import ChatOpenRouter

from src.config.config import get_api_key
from src.knowledge_base.file_processor import process_files, create_text_chunks
from src.knowledge_base.chroma_embeddings import create_vector_store
from src.dao.metrics_dao import save_rag_metrics_db


load_dotenv()
vector_store = create_vector_store()

def initialize_knowledge_base():
    global vector_store
    if vector_store._collection.count() == 0:
        print("Servindo arquivo principal para o chroma_db...")
        my_text = process_files()
        if my_text:
            chunks = create_text_chunks(my_text)
            vector_store = create_vector_store(chunks)
            print(f"Sucesso ao criar o vector_store com {len(chunks)} chunks.")
            
initialize_knowledge_base()

def send_message_api_logic(chat_history, session_id):
    api_key = get_api_key() or os.getenv("API_KEY")

    llm = ChatOpenRouter(
        model="openrouter/free", 
        api_key=api_key,
        temperature=0.7
    )

    last_user_message = next(
        (m["content"] for m in reversed(chat_history) if m["role"] == "user"),
        None
    )

    context_text = ""
    vector_search_start_time = 0

    if last_user_message:
        start_time = time.time()
        docs = vector_store.similarity_search(last_user_message, k=3)
        vector_search_time_ms = int((time.time() - start_time) * 1000)
        if docs:
            context_text = "\n\n".join(d.page_content for d in docs)

    system_instruction = {
        "role": "system",
        "content": """Você é o Lumyn, uma inteligência artificial prestativa, inteligente e amigável. 
        Nunca diga que é o ChatGPT, OpenAI ou um modelo genérico. Seu nome é estritamente Lumyn. 
        Responda perguntas sobre você SOMENTE com base no contexto relevante fornecido abaixo, quando disponível.
        Se a pergunta for sobre detalhes técnicos (linguagem de programação, modelo de IA 
        específico, infraestrutura) e essa informação não estiver no contexto abaixo, 
        diga claramente que não tem essa informação disponível, em vez de tentar adivinhar.
        CASO a pergunta não seja sobre você, responda normalmente com base no seu conhecimento geral.""" 
        + (f"\n\nContexto relevante:\n{context_text}" if context_text else "")
    }

    full_messages = [system_instruction] + chat_history

    try:
        start_llm_time = time.time()
        response = llm.invoke(full_messages)
        llm_response_time_ms = int((time.time() - start_llm_time) * 1000)

        total_response_time_ms = llm_response_time_ms + vector_search_time_ms

        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        tokens_usage = getattr(response, "response_metadata", {}).get("token_usage", {})
        if tokens_usage:
            prompt_tokens = tokens_usage.get("prompt_tokens", 0)
            completion_tokens = tokens_usage.get("completion_tokens", 0)
            total_tokens = tokens_usage.get("total_tokens", 0)

        save_rag_metrics_db(
            session_id=session_id,
            response_time_ms=total_response_time_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            vector_search_time_ms=vector_search_time_ms
        )

        return response.content if response else None

    except Exception as e:   
        print(f"(API) Erro ao tentar conectar com o modelo: {e}")
        return None