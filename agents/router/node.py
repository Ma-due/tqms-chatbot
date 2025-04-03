# agents/router.py
from utils import get_llm
from state import GraphState
from agents.router.prompt import router_prompt_template, dictionary_prompt_template, human_dictionary
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

AVAILABLE_TOOLS = ["web", "db", "vectordb"]

def analyze_intent(question: str, chat_history) -> str:
    llm = get_llm()
    intent_prompt = ChatPromptTemplate.from_messages([
        ("system", "질문과 대화 히스토리를 보고 사용자의 의도를 한 문장으로 요약하세요."),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}")
    ])
    chain = intent_prompt | llm | StrOutputParser()
    return chain.invoke({"question": question, "chat_history": chat_history})

def contextualize_query(question: str, chat_history) -> str:
    llm = get_llm()
    intent = analyze_intent(question, chat_history)  # 의도 분석
    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system", "다음 의도를 유지하며, 히스토리 없이도 독립적으로 이해 가능한 단일 질문을 재구성하세요: {intent}\n답변은 생성하지 말고, 질문만 반환하세요."),
        ("human", "{question}")
    ])
    chain = contextualize_prompt | llm | StrOutputParser()
    return chain.invoke({"question": question, "intent": intent, "chat_history": chat_history})

def apply_dictionary(question: str) -> str:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(dictionary_prompt_template)
    dictionary_chain = prompt | llm | StrOutputParser()
    return dictionary_chain.invoke({
        "question": question,
        "dictionary": human_dictionary
    })

def router_node(state: GraphState) -> GraphState:
    llm = get_llm()
    chat_history = state["chat_history"]
    question = state["question"]

    print("원본 question: ", question)
    # 최초 질문에만 사전 적용
    if not chat_history:  # 히스토리가 비어 있으면 (최초 질문)
        question = apply_dictionary(question)
        print("dictionary 적용 후 question: ", question)
    else:
        # 히스토리로 질문 재구성
        question = contextualize_query(question, chat_history)
    
    print("contextualize_query 적용 후 question: ", question)
    # 경로 선택
    prompt = ChatPromptTemplate.from_template(router_prompt_template)
    router_chain = prompt | llm | StrOutputParser()
    route = router_chain.invoke({
        "question": question,
        "tools": ", ".join(AVAILABLE_TOOLS)
    }).strip("[]")

    print("router_chain.invoke 결과: ", route)

    # 상태 업데이트
    state["question"] = question
    state["route"] = route
    return state