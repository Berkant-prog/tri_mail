"""Build and compile the LangGraph workflow for email processing."""

from langgraph.graph import END, START, StateGraph

from mail_agent.nodes.critique import critique_node, critique_route
from mail_agent.nodes.draft import draft_node
from mail_agent.nodes.human_review import human_review_node, human_review_route
from mail_agent.nodes.triage import triage_node
from mail_agent.state import MailAgentState


def build_graph() -> StateGraph:
    """Create the uncompiled graph definition with placeholder routing."""

    graph = StateGraph(MailAgentState)
    graph.add_node("triage", triage_node)
    graph.add_node("draft", draft_node)
    graph.add_node("critique", critique_node)
    graph.add_node("human_review", human_review_node)

    graph.add_edge(START, "triage")
    # TODO: add conditional edges from triage to draft or END.
    # TODO: add the draft -> critique edge.
    # TODO: add conditional edges from critique to draft or human_review.
    # TODO: add conditional edges from human_review to send, edit, or reject.

    return graph


def compile_graph() -> object:
    """Compile the graph; configure the Postgres checkpointer here later."""

    graph = build_graph()
    # TODO: create AsyncPostgresSaver/connection from Settings.postgres_dsn.
    # TODO: pass the Postgres checkpointer to graph.compile(checkpointer=...).
    return graph.compile()