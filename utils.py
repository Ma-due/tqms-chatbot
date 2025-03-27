# utils.py
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import contextualize_q_system_prompt
from langchain_chroma import Chroma

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


def get_retriever():
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    persist_directory = "./chroma_db"
    database = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding,
        collection_name="tqms"
    )
    # index_name = 'tqms'
    # database = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
    retriever = database.as_retriever(search_kwargs={'k': 4})
    return retriever


def get_llm(model='gpt-4o'):
    llm = ChatOpenAI(model=model)
    return llm


def get_history_retriever():
    llm = get_llm()
    retriever = get_retriever()
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever
