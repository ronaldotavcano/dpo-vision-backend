class InvalidDocumentError(Exception):
    """The input is not a readable, non-empty PDF."""


class OcrUnavailableError(Exception):
    """The OCR engine or its language data is unavailable."""


class SemanticSearchUnavailableError(Exception):
    """The semantic analysis service is unavailable or returned invalid data."""
