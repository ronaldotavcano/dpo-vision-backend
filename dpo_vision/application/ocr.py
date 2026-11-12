from dataclasses import dataclass
import unicodedata
from dpo_vision.application.ports import DocumentOcrPort, SemanticSearchPort
from dpo_vision.domain.models import DocumentOcr


@dataclass
class ProcessDocument:
    processor: DocumentOcrPort

    def execute(self, content: bytes) -> DocumentOcr:
        return self.processor.process(content)


@dataclass
class AnalyzeDocument:
    processor: DocumentOcrPort
    searcher: SemanticSearchPort

    def execute(self, content: bytes, prompt: str) -> tuple[DocumentOcr, list[dict]]:
        document = self.processor.process(content)
        words = document.words()
        text = " ".join(word["texto"] for word in words)
        selections = self.searcher.search(text, prompt)
        selected = set()

        def normalize(value: str) -> str:
            value = value.casefold()
            while value and unicodedata.category(value[0]).startswith("P"):
                value = value[1:]
            while value and unicodedata.category(value[-1]).startswith("P"):
                value = value[:-1]
            return value

        normalized_words = [normalize(word["texto"]) for word in words]
        for selection in selections:
            tokens = [normalize(token) for token in selection.split()]
            tokens = [token for token in tokens if token]
            if not tokens:
                continue
            for start in range(len(words) - len(tokens) + 1):
                end = start + len(tokens)
                if (normalized_words[start:end] == tokens
                        and words[start]["pagina"] == words[end - 1]["pagina"]):
                    selected.update(range(start, end))
        return document, [word for index, word in enumerate(words) if index in selected]
