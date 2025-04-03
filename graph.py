# graph.py
from langgraph.graph import StateGraph, END
from state import GraphState
from agents.router.node import router_node
from agents.vectordb.node import retrieve_node
from agents.answer.node import answer_node
from utils import get_session_history

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("router", router_node)
    graph.add_node("vectordb", retrieve_node)
    graph.add_node("web", lambda state: state)  # 임시 노드 (아직 구현 안 됨)
    graph.add_node("db", lambda state: state)   # 임시 노드 (아직 구현 안 됨)
    graph.add_node("generate_answer", answer_node)

    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {"vectordb": "vectordb", "web": "web", "db": "db"}
    )
    graph.add_edge("vectordb", "generate_answer")
    graph.add_edge("web", "generate_answer")
    graph.add_edge("db", "generate_answer")
    graph.add_edge("generate_answer", END)

    graph.set_entry_point("router")
    return graph.compile()

def get_ai_response(user_message: str):
    graph = build_graph()
    initial_history = get_session_history("abc123").messages
    result = graph.invoke({"question": user_message, "chat_history": initial_history})
    return result["response"]