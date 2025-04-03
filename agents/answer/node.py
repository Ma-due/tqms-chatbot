# agents/answer.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import get_llm, get_session_history
from agents.answer.prompt import system_prompt
from state import GraphState

def answer_node(state: GraphState) -> GraphState:
    llm = get_llm()
    chat_history = get_session_history("abc123")  # 업데이트용으로만 사용

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "질문: {question}")
    ])

    results = "\n".join([doc.page_content for doc in state["results"]]) if state["results"] else "결과 없음"
    chain = qa_prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "question": state["question"],
        "context": results,
    })

    # 히스토리 업데이트
    chat_history.add_user_message(state["question"])
    chat_history.add_ai_message(answer)
    return {"response": answer, "chat_history": chat_history.messages}