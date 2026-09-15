"""Tests for the draft node contract."""

from mail_agent.nodes.draft import draft_node
from mail_agent.state import MailAgentState


def test_draft_increments_iteration_count() -> None:
    """Drafting exposes the iteration counter in its state update."""

    assert draft_node(MailAgentState(iteration_count=2))["iteration_count"] == 3