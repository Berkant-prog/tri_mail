"""Triage node: classify a thread as important or not important.

Input: :class:`MailAgentState.thread`.
Output: a partial state containing ``triage_result``.
Conditional edge: ``graph.py`` routes ``important`` to drafting and
``not_important`` to the terminal path.
"""

from mail_agent.state import MailAgentState


def triage_node(state: MailAgentState) -> dict[str, str]:
    """Return a placeholder triage result for the current thread."""

    return {"triage_result": "important"}