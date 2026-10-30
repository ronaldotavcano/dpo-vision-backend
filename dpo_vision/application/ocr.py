from dataclasses import dataclass
from dpo_vision.application.ports import DocumentOcrPort
from dpo_vision.domain.models import DocumentOcr


@dataclass
class ProcessDocument:
    processor: DocumentOcrPort

    def execute(self, content: bytes) -> DocumentOcr:
        return self.processor.process(content)
