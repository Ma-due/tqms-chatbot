from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from utils import get_llm, get_session_history, get_history_retriever
from config import human_dictionary, tqms_system_prompt, tqms_example_answer
from lg.types.state import GraphState
from lg.nodes.dictionary import dictionary_node
from lg.nodes.retrieve import retrieve_node
from lg.nodes.generate import generate_answer_node


# 상태 정의
class GraphState(TypedDict):
    question: str
    modified_question: str
    search_results: list
    answer: str
    chat_history: Annotated[Sequence[BaseMessage], "chat_history"]


# 노드 정의
def dictionary_node(state: GraphState) -> GraphState:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(f"""
        사용자의 질문을 보고, 우리의 사전을 참고해서 사용자의 질문을 변경해주세요.
        만약 변경할 필요가 없다고 판단된다면, 사용자의 질문을 변경하지 않아도 됩니다.
        그런 경우에는 질문만 리턴해주세요
        사전: {human_dictionary}

        질문: {{question}}
    """)
    dictionary_chain = prompt | llm | StrOutputParser()
    modified_question = dictionary_chain.invoke({"question": state["question"]})
    return {"modified_question": modified_question}


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


def generate_answer_node(state: GraphState) -> GraphState:
    llm = get_llm()
    chat_history = get_session_history("abc123")

    # Few-shot 프롬프트 설정
    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{answer}")]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=tqms_example_answer,
    )

    # 검색 결과를 context로 포함하도록 프롬프트 수정
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", tqms_system_prompt),  # system_prompt에 {context}가 있다고 가정
            few_shot_prompt,
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # 검색 결과를 문자열로 변환
    context = "\n".join([doc.page_content for doc in state["search_results"]])

    # 체인 실행
    chain = qa_prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "input": state["modified_question"],
        "chat_history": chat_history.messages if chat_history.messages else state["chat_history"],
        "context": context  # 검색 결과를 context로 전달
    })

    # 히스토리 업데이트
    chat_history.add_user_message(state["modified_question"])
    chat_history.add_ai_message(answer)

    return {"answer": answer, "chat_history": chat_history.messages}


# 그래프 구성
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("dictionary", dictionary_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate_answer", generate_answer_node)

    graph.set_entry_point("dictionary")
    graph.add_edge("dictionary", "retrieve")
    graph.add_edge("retrieve", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


def get_ai_response(user_message: str):
    graph = build_graph()
    initial_history = get_session_history("abc123").messages
    result = graph.invoke({"question": user_message, "chat_history": initial_history})
    return result["answer"]