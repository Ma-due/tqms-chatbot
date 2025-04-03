#agents/vectordb/retriever.py
from utils import get_llm
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_chroma import Chroma
from langchain.chains import create_history_aware_retriever
from agents.vectordb.prompt import contextualize_q_system_prompt


def get_retriever():
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    persist_directory = "./chroma_db"
    database = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding,
        collection_name="tqms"
    )
    retriever = database.as_retriever(search_kwargs={'k': 4})
    return retriever


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
    # 대화 히스토리를 고려하여 검색할 수 있는 retriever를 생성합니다.
    # llm: 대화 맥락을 이해하고 질문을 재구성하는데 사용되는 언어 모델
    # retriever: 실제 문서 검색을 수행하는 기본 retriever
    # contextualize_q_prompt: 대화 히스토리를 바탕으로 질문을 재구성하는 프롬프트
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever
