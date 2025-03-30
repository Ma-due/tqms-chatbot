from utils import get_history_retriever
from lg.types.state import GraphState

def retrieve_node(state: GraphState) -> GraphState:
    retriever = get_history_retriever()
    # 대화 히스토리를 기반으로 검색
    search_results = retriever.invoke({
        "input": state["modified_question"],
        "chat_history": state["chat_history"]
    })
    print(f"벡터 DB 검색 결과 (쿼리: {state['modified_question']}):")
    for i, result in enumerate(search_results, 1):
        print(f"[{i}] {result.page_content}")
        print(f"메타데이터: {result.metadata}")
        print("---")
    return {"search_results": search_results} 