from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.agents.cleaning_agent import cleaning_agent
from src.agents.keyword_agent import keyword_agent
from src.agents.linkedin_writer_agent import writer_agent
from src.agents.reviewer_agent import reviewer_agent
from src.agents.rewrite_agent import rewrite_agent
from src.config import Config
from src.pipeline.state import AgentState


def route_review(state: AgentState):
    score = int(state.get("score", 0))
    rewrites = int(state.get("rewrite_round", 0))

    if score >= Config.REVIEW_SCORE_THRESHOLD:
        return END

    if rewrites >= Config.MAX_REWRITE_ROUNDS:
        return END

    return "rewrite"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("clean", cleaning_agent)
    graph.add_node("keywords", keyword_agent)
    graph.add_node("write", writer_agent)
    graph.add_node("review", reviewer_agent)
    graph.add_node("rewrite", rewrite_agent)

    graph.set_entry_point("clean")
    graph.add_edge("clean", "keywords")
    graph.add_edge("keywords", "write")
    graph.add_edge("write", "review")

    graph.add_conditional_edges("review", route_review)
    graph.add_edge("rewrite", "review")

    return graph.compile()
