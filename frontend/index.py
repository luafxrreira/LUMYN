import streamlit as st
import random

responses_list = ["OK", "Legal", "Show", "Tudo bem", "Tem certeza?"]

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if st.session_state["page"] == "home":
        st.header("LUMYN")
        st.markdown("---")
        with st.container(height=600, border=False):
            st.write("### Escreva, interaja, converse e tire dúvidas com o lumyn.")
        
        initial_prompt = st.chat_input("Qual é o país com mais copas vencidas?")
        if initial_prompt:
            st.session_state["messages"].append({"role": "user", "content": initial_prompt})
            st.session_state["messages"].append({"role": "assistant", "content": random.choice(responses_list)})
            st.session_state["page"] = "chat"
            st.rerun()

    elif st.session_state["page"] == "chat":
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader("CHAT LUMYN")
        with col2:
            if st.button("Voltar", type="secondary", use_container_width=True):
                st.session_state["messages"] = []
                st.session_state["page"] = "home"
                st.rerun()
            
        st.markdown("---")

        with st.container(height=600, border=False):
            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        follow_up_prompt = st.chat_input("Pergunte algo mais...")
        if follow_up_prompt:
            st.session_state["messages"].append({"role": "user", "content": follow_up_prompt})
            st.session_state["messages"].append({"role": "assistant", "content": random.choice(responses_list)})
            st.rerun()

main()