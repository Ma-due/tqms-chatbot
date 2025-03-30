from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    question: str
    modified_question: str
    search_results: list
    answer: str
    chat_history: Annotated[Sequence[BaseMessage], "chat_history"] 