"""Triage node: classify a thread as important or not important.

Input: :class:`MailAgentState.thread`.
Output: a partial state containing ``triage_result`` and ``triage_method``.
Conditional edge: ``graph.py`` routes ``important`` to drafting and
``not_important`` to the terminal path.
"""

from typing import Literal

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from mail_agent.state import MailAgentState

TriageResult = Literal["critical", "high", "medium", "low", "not_important"]

# --- Heuristics config -------------------------------------------------

VIP_SENDERS: set[str] = set()  # emails/domaines toujours importants
URGENT_KEYWORDS = {"urgent", "deadline", "asap", "contrat", "facture"}
NOISE_SENDER_PATTERNS = {"noreply@", "no-reply@", "newsletter@"}


class TriageDecision(BaseModel):
    priority: TriageResult
    needs_reply: bool = Field(description="True if the thread requires a personal response")
    reason: str = Field(description="One-sentence justification")


def _heuristic_triage(thread) -> TriageResult | None:
    """Fast, deterministic pass. Returns None if ambiguous (needs the LLM)."""

    sender = thread.sender.lower()
    subject = thread.subject.lower()

    if any(p in sender for p in NOISE_SENDER_PATTERNS):
        return "not_important"
    if sender in VIP_SENDERS:
        return {"priority": "critical", "needs_reply": True, "reason": "VIP sender"}
    if any(keyword in subject for keyword in URGENT_KEYWORDS):
        return {"priority": "critical", "needs_reply": True, "reason": "Urgent keyword found"}

    return None  # ambigu — on laisse le LLM trancher


_llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0).with_structured_output(
    TriageDecision
)

_TRIAGE_PROMPT = """Tu tries un thread e-mail pour {user}.

1. Donne une priorité : critical / high / medium / low / not_important
2. Donne needs_reply=false UNIQUEMENT si tu es quasi certain qu'aucune
   réponse n'est attendue (notification automatisée, newsletter, accusé
   de réception, spam). En cas de doute, needs_reply=true — mieux vaut
   un brouillon inutile qu'une réponse manquée.

De : {sender}
Objet : {subject}
Corps (tronqué) :
{body}
"""


def _llm_triage(thread) -> TriageDecision:
    decision = _llm.invoke(
        _TRIAGE_PROMPT.format(
            user="Berkant",
            sender=thread.sender,
            subject=thread.subject,
            body=thread.body[:1000],
        )
    )
    return decision



def triage_node(state: MailAgentState) -> TriageDecision:
    """Classify state.thread, heuristics first, LLM as fallback."""

    result = _heuristic_triage(state.thread)
    if result is not None:
        return {**result, "triage_method": "heuristic"}

    decision = _llm_triage(state.thread)
    return {
        "priority": decision.priority,
        "needs_reply": decision.needs_reply,
        "triage_method": "llm",
        "reason": decision.reason,
    }