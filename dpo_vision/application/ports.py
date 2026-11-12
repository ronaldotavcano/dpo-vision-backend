from typing import Protocol
from dpo_vision.domain.models import DocumentOcr


class DocumentOcrPort(Protocol):
    def process(self, content: bytes) -> DocumentOcr: ...


class SemanticSearchPort(Protocol):
    """Select text from the document relevant to a user's query."""

    def search(self, text: str, query: str) -> list[str]: ...
