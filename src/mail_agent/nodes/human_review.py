"""Human-review node: pause the graph until a person validates the draft.

Input: :class:`MailAgentState.draft` and the accumulated ``edit_history``.
Output: an interrupt payload; after resumption, the decision routes to
``send``, ``edit``, or ``reject``. The API resumes this node with a LangGraph
``Command``.
Conditional edge: ``human_review_route`` maps the human decision to the
corresponding terminal or edit path.
"""

from typing import Literal

from pydantic import BaseModel, ValidationError
from langgraph.types import interrupt

from mail_agent.state import MailAgentState

HumanAction = Literal["send", "edit", "reject"]


class HumanResumePayload(BaseModel):
    """Expected shape of the value sent back via Command(resume=...)."""

    action: HumanAction
    edited_draft: str | None = None  # required when action == "edit"


def human_review_node(state: MailAgentState) -> dict[str, object]:
    """Pause execution with the current draft for human validation."""

    raw = interrupt({"draft": state.draft, "message": "Review the draft."})

    try:
        payload = HumanResumePayload.model_validate(raw)
    except ValidationError as exc:
        # Ne jamais router silencieusement sur une valeur invalide —
        # un bug côté API de reprise doit être visible, pas absorbé en "reject".
        raise ValueError(f"Invalid human review payload: {raw!r}") from exc

    update: dict[str, object] = {"human_decision": payload.action}

    if payload.action == "edit":
        if not payload.edited_draft:
            raise ValueError("action='edit' requires 'edited_draft' to be set")
        update["draft"] = payload.edited_draft
        update["edit_history"] = state.edit_history + [
            {"original": state.draft, "edited": payload.edited_draft}
        ]

    return update


def human_review_route(state: MailAgentState) -> Literal["send", "edit", "reject"]:
    """Return the next route selected by the human reviewer."""

    return state.human_decision