"""Pydantic state models shared by the mail-agent graph nodes."""

from typing import Literal

from pydantic import BaseModel, Field


class MailMessage(BaseModel):
    """Minimal representation of a message in an email thread."""

    message_id: str
    sender: str = ""
    recipients: list[str] = Field(default_factory=list)
    subject: str = ""
    body: str = ""


class EditRecord(BaseModel):
    """One human or automated modification made to a draft."""

    instruction: str
    resulting_draft: str
    author: Literal["human", "agent"] = "human"


class MailAgentState(BaseModel):
    """State carried through triage, drafting, critique, and human review.

    The model is intentionally small: fields can be extended as Gmail metadata,
    critique details, and approval policies become concrete.
    """

    thread: list[MailMessage] = Field(default_factory=list)
    draft: str | None = None
    iteration_count: int = 0
    edit_history: list[EditRecord] = Field(default_factory=list)
    triage_result: Literal["important", "not_important"] | None = None
    human_decision: Literal["send", "edit", "reject"] | None = None