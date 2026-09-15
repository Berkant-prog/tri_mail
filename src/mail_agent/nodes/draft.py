"""Draft node: create or revise a reply to an important email thread.

Input: :class:`MailAgentState.thread`, ``draft``, and ``edit_history``.
Output: a partial state containing a draft and incremented iteration count.
Conditional edge: the critique node decides whether to return here for another
draft or continue to human review.
"""

from mail_agent.state import MailAgentState


def draft_node(state: MailAgentState) -> dict[str, object]:
    """Return a placeholder draft while preserving the graph contract."""

    return {
        "draft": state.draft or "[Draft placeholder]",
        "iteration_count": state.iteration_count + 1,
    }