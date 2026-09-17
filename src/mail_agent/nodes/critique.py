"""Critique node: internally assess a draft before human validation.

Input: :class:`MailAgentState.draft`, ``thread``, and ``iteration_count``.
Output: a routing decision, either ``draft`` for revision or ``human_review``.
Conditional edge: this node owns the critique-to-draft or critique-to-review
decision; the concrete quality checks are intentionally left as a stub.
"""

from typing import Literal

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from mail_agent.state import MailAgentState

MAX_CRITIQUE_ITERATIONS = 2


class CritiqueResult(BaseModel):
    """The result of a critique, including the next node to visit."""

    critique_route: Literal["draft", "human_review"]
    review_summary: str = Field(
        default="", description="A brief summary of the critique."
    )


_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
    max_tokens=500,
).with_structured_output(CritiqueResult)

_CRITIQUE_PROMPT = """Relis ce brouillon de réponse par rapport au fil d'origine.
Vérifie : ton adapté, réponse aux points soulevés, pas d'info manquante ou inventée.

Fil original :
{thread}

Brouillon :
{draft}

Si le brouillon est correct, route="human_review". Sinon, route="draft" et explique
en une phrase ce qui doit être corrigé.
"""


def critique_node(state: MailAgentState) -> dict[str, object]:
    """Critique the draft, forcing human_review past the iteration cap."""

    if state.iteration_count >= MAX_CRITIQUE_ITERATIONS:
        return {
            "critique_route": "human_review",
            "review_summary": "Iteration cap reached — forwarding as-is.",
            "iteration_count": state.iteration_count + 1,
        }

    result = _llm.invoke(
        _CRITIQUE_PROMPT.format(thread=state.thread, draft=state.draft)
    )

    return {
        "critique_route": result.critique_route,
        "review_summary": result.review_summary,
        "iteration_count": state.iteration_count + 1,
    }


def critique_route(state: MailAgentState) -> Literal["draft", "human_review"]:
    """Route based on the critique's own decision."""

    return state.critique_route