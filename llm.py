# main.py
from utils import get_llm, get_history_retriever
from chains import get_dictionary_chain, get_rag_chain

def get_ai_response(user_message):
    llm = get_llm()
    history_aware_retriever = get_history_retriever()
    dictionary_chain = get_dictionary_chain(llm)
    rag_chain = get_rag_chain(llm, history_aware_retriever)
    tax_chain = {"input": dictionary_chain} | rag_chain

    # 검색 결과 출력
    search_results = history_aware_retriever.invoke({"input": user_message})
    print(f"벡터 DB 검색 결과 (쿼리: {user_message}):")
    for i, result in enumerate(search_results, 1):
        print(f"[{i}] {result.page_content}")
        print(f"메타데이터: {result.metadata}")
        print("---")

    ai_response = tax_chain.stream(
        {
            "question": user_message
        },
        config={
            "configurable": {"session_id": "abc123"}
        },
    )
    return ai_response