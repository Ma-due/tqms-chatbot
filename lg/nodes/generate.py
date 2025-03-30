from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import get_llm, get_session_history
from config import tqms_system_prompt, tqms_example_answer
from lg.types.state import GraphState

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
            ("system", tqms_system_prompt),
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
        "context": context
    })

    # 히스토리 업데이트
    chat_history.add_user_message(state["modified_question"])
    chat_history.add_ai_message(answer)

    return {"answer": answer, "chat_history": chat_history.messages} 