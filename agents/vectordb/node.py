# agents/vectordb/vectordb.py
from state import GraphState
from agents.vectordb.retriever import get_retriever  # get_history_retriever 대신 기본 retriever
from agents.common.common import get_few_shot_prompt
from utils import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.vectordb.prompt import example_answer
from typing import Dict, Any


# LLM 기반 키워드 추출 함수
def extract_keywords_with_llm(query: str, llm) -> str:
    prompt = ChatPromptTemplate.from_template(
        "다음 질문에서 핵심 키워드만 추출하세요. 단어 사이에 공백을 넣고, 불필요한 조사는 제외하세요.\n"
        "질문: {query}"
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query})


def retrieve_node(state: GraphState) -> Dict[str, Any]:
    print("벡터 DB 검색 시작")
    llm = get_llm()
    retriever = get_retriever()  # 히스토리 처리 없는 기본 retriever

    # LLM 기반 키워드 추출 추가
    keyword_query = extract_keywords_with_llm(state["question"], llm)
    print(f"LLM 키워드 추출 쿼리: {keyword_query}")

    # 키워드 쿼리로 벡터 DB 검색
    results = retriever.invoke(keyword_query)  # optimized_query 대신 keyword_query 사용

    print(f"벡터 DB 검색 결과 (원본 쿼리: {state['question']}, 검색 쿼리: {keyword_query}):")
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result.page_content}")
        print(f"메타데이터: {result.metadata}")
        print("---")

    return {"results": results}