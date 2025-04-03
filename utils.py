# utils.py
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    # store 상태 출력
    print("현재 store 상태:")
    if not store[session_id].messages:
        print(f"  세션 ID: {session_id}, [히스토리 없음, 빈 리스트]")
    else:
        print(f"  세션 ID: {session_id}의 대화 히스토리:")
        for i, msg in enumerate(store[session_id].messages):
            print(f"    [{i}] {msg.type}: {msg.content}")

    return store[session_id]


def get_llm(model='gpt-4o', temperature=0.0):
    llm = ChatOpenAI(model=model, temperature=temperature)
    return llm