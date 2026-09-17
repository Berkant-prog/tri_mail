"""Draft node: create or revise a reply to an important email thread.

Input: :class:`MailAgentState.thread`, ``draft``, and ``review_summary``.
Output: a partial state containing the (re)generated draft.
Conditional edge: the critique node decides whether to return here for another
draft or continue to human review. ``iteration_count`` is owned by
``critique_node``, not incremented here.
"""

from mail_agent.state import MailAgentState


def draft_node(state: MailAgentState) -> dict[str, object]:
    """Generate a fresh draft, or revise using the critique's feedback."""

    if state.review_summary:
        # On revient d'une critique négative : réviser en tenant compte du retour.
        prompt_context = f"Previous feedback: {state.review_summary}"
    else:
        prompt_context = "First draft."

    # TODO: remplacer par un vrai appel LLM avec state.thread + prompt_context
    return {"draft": f"[Draft placeholder — {prompt_context}]"}