from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import get_llm
from config import human_dictionary
from lg.types.state import GraphState

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