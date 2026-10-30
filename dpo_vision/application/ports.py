from typing import Protocol
from dpo_vision.domain.models import DocumentOcr


class DocumentOcrPort(Protocol):
    def process(self, content: bytes) -> DocumentOcr: ...


class SemanticSearchPort(Protocol):
    """Future provider for locating relevant text within a document."""

    def search(self, document: DocumentOcr, query: str) -> list[dict]: ...
