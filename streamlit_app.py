import streamlit as st
from lg.graph import get_ai_response

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    if prompt := st.chat_input("질문을 입력하세요"):
        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성 및 표시
        with st.chat_message("assistant"):
            response = get_ai_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.title("TQMS 챗봇")
    init_session_state()
    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    main() 