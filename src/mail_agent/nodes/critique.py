"""Critique node: internally assess a draft before human validation.

Input: :class:`MailAgentState.draft`, ``thread``, and ``iteration_count``.
Output: a routing decision, either ``draft`` for revision or ``human_review``.
Conditional edge: this node owns the critique-to-draft or critique-to-review
decision; the concrete quality checks are intentionally left as a stub.
"""

from typing import Literal

from mail_agent.state import MailAgentState


def critique_node(state: MailAgentState) -> dict[str, object]:
    """Return a placeholder critique result without implementing policy."""

    return {"critique_route": "human_review"}


def critique_route(state: MailAgentState) -> Literal["draft", "human_review"]:
    """Choose the next node after critique using a placeholder policy."""

    return "human_review"