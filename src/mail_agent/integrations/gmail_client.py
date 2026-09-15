"""Small Gmail API wrapper boundary for reading threads and sending mail."""

from collections.abc import Sequence

from mail_agent.state import MailMessage


class GmailClient:
    """Own Gmail OAuth setup and expose application-facing mail operations."""

    def __init__(self, client_secret_file: str, token_file: str) -> None:
        """Store OAuth file locations; authentication is intentionally deferred."""

        self.client_secret_file = client_secret_file
        self.token_file = token_file

    def authenticate(self) -> None:
        """Authenticate with Gmail OAuth and prepare the API service."""

        raise NotImplementedError

    def read_thread(self, thread_id: str) -> Sequence[MailMessage]:
        """Read a Gmail thread and return normalized messages."""

        raise NotImplementedError

    def send_message(self, message: MailMessage) -> str:
        """Send a message through Gmail and return its provider identifier."""

        raise NotImplementedError