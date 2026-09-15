"""Human-review node: pause the graph until a person validates the draft.

Input: :class:`MailAgentState.draft` and the accumulated ``edit_history``.
Output: an interrupt payload; after resumption, the decision routes to
``send``, ``edit``, or ``reject``. The API resumes this node with a LangGraph
``Command``.
Conditional edge: ``human_review_route`` maps the human decision to the
corresponding terminal or edit path.
"""

from typing import Literal

from langgraph.types import interrupt

from mail_agent.state import MailAgentState


def human_review_node(state: MailAgentState) -> dict[str, object]:
    """Pause execution with the current draft for human validation."""

    decision = interrupt({"draft": state.draft, "message": "Review the draft."})
    return {"human_decision": decision}


def human_review_route(state: MailAgentState) -> Literal["send", "edit", "reject"]:
    """Return the next route selected by the human reviewer."""

    return state.human_decision or "reject"