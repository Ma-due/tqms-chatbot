import streamlit as st
from graph import get_ai_response

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    if prompt := st.chat_input("질문을 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # get_ai_response로 바로 처리
        with st.chat_message("assistant"):
            response = get_ai_response(prompt)  # routing_info 제거
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.title("TQMS 챗봇")
    init_session_state()
    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    main()