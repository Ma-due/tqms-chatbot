#state.py
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    question: str
    results: list
    response: str
    chat_history: Annotated[Sequence[BaseMessage], "chat_history"] 