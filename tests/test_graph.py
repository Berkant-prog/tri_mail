"""Tests for graph construction."""

from mail_agent.graph import build_graph


def test_graph_contains_expected_nodes() -> None:
    """The initial graph skeleton registers all workflow nodes."""

    graph = build_graph()
    assert {"triage", "draft", "critique", "human_review"} <= set(graph.nodes)