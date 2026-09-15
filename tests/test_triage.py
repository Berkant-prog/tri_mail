"""Tests for the triage node contract."""

from mail_agent.nodes.triage import triage_node
from mail_agent.state import MailAgentState


def test_triage_returns_a_route() -> None:
    """The triage stub returns a valid state update."""

    assert triage_node(MailAgentState()) == {"triage_result": "important"}