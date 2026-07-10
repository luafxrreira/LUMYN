import streamlit as st
import requests, os, uuid

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001")

API_SEND = f"{BACKEND_URL}/chat/send"
API_HISTORY = f"{BACKEND_URL}/chat/history"
REQUEST_TIMEOUT = 15

def main():

    st.set_page_config(page_title="Lumyn - Chat AI", page_icon=":robot:", layout="wide")

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    
    actual_session_id = st.session_state.session_id
    response = requests.get(f"{BACKEND_URL}/session", params={"session_id" : actual_session_id}, timeout=REQUEST_TIMEOUT)

    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    if st.session_state["page"] == "home":
        st.header("LUMYN")
        st.markdown(
            """
            :gray-badge[ O Lumyn é um modelo de linguagem baseado em inteligência artificial. Ele pode fornecer informações úteis,]
            :gray-badge[mas não substitui aconselhamento profissional. Sempre verifique as informações obtidas.]
            """
        )
        st.markdown("---")
        with st.container(height=500, border=False):
            st.write("### Escreva, interaja, converse e tire dúvidas com o Lumyn.")
        
            
            st.markdown(":gray-badge[Caso a resposta tenha algum problema de tempo excedido, por favor, tente enviá-la novamente.]")

        initial_prompt = st.chat_input("Qual é o país com mais copas vencidas?")
        if initial_prompt:
            payload = {
                "query": initial_prompt,
                "session_id": actual_session_id,
                "user_id": 1
            }
            with st.spinner("Processando sua pergunta pelo Lumyn...", show_time=True):
                try:
                    response = requests.post(API_SEND, json=payload, timeout=REQUEST_TIMEOUT)
                    if response.status_code == 200:
                        st.session_state["page"] = "chat"
                        st.rerun()
                    else:
                        st.error("Erro ao iniciar conversa com o servidor.")
                except Exception as e:
                    st.error(f"Não foi possível conectar com o servidor: {str(e)}")

    elif st.session_state["page"] == "chat":
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader("CHAT LUMYN")
        with col2:
            if st.button("Voltar", type="secondary", use_container_width=True):
                st.session_state["page"] = "home"
                st.rerun()
            
        st.markdown("---")

        messages = []
        try:
            response = requests.get(API_HISTORY, params={"session_id": actual_session_id}, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data_obtained = response.json()
                messages = data_obtained.get("historico", [])
            else:
                st.error("Erro ao buscar histórico.")
        except Exception as e:
            st.error(f"Erro ao buscar histórico: {str(e)}")

        with st.container(height=500, border=False):
            if not messages:
                st.info("Nenhuma mensagem encontrada no histórico.")
            else:
                for message in messages:
                    role = message.get("role", "assistant")
                    content = message.get("content", "")
                    with st.chat_message(role):
                        st.write(content)
      
            follow_up_prompt = st.chat_input("Pergunte algo mais...")
            if follow_up_prompt:
                payload = {
                    "query": follow_up_prompt,
                    "session_id": actual_session_id,
                    "user_id": 1
                }
                with st.spinner("Processando sua pergunta pelo Lumyn...", show_time=True):
                    try:
                        response = requests.post(API_SEND, json=payload)
                        if response.status_code == 200:
                            st.rerun()
                        else:
                            st.error("Erro ao obter resposta do servidor.")
                    except Exception as e:
                        st.error(f"Erro ao enviar mensagem: {str(e)}")

if __name__ == "__main__":
    main()