# utils.py
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import contextualize_q_system_prompt

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_retriever():
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    index_name = 'tqms'
    database = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
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