import io
import os

import pymupdf
import pytesseract
from PIL import Image

from dpo_vision.domain.errors import InvalidDocumentError, OcrUnavailableError
from dpo_vision.domain.models import DocumentOcr, PageOcr


class TesseractPdfProcessor:
    def __init__(self, language: str | None = None, executable: str | None = None):
        self.language = language or os.getenv("TESSERACT_LANG", "por")
        executable = executable or os.getenv("TESSERACT_CMD")
        if executable:
            pytesseract.pytesseract.tesseract_cmd = executable

    def process(self, content: bytes) -> DocumentOcr:
        if not content:
            raise InvalidDocumentError("O PDF est? vazio.")
        try:
            document = pymupdf.open(stream=content, filetype="pdf")
        except (pymupdf.FileDataError, ValueError) as exc:
            raise InvalidDocumentError("O arquivo n?o ? um PDF v?lido.") from exc
        try:
            if document.needs_pass:
                raise InvalidDocumentError("PDF protegido por senha n?o ? suportado.")
            if document.page_count == 0:
                raise InvalidDocumentError("O PDF n?o cont?m p?ginas.")
            pages = []
            for index, page in enumerate(document):
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(300 / 72, 300 / 72))
                with Image.open(io.BytesIO(pixmap.tobytes("png"))) as image:
                    try:
                        data = pytesseract.image_to_data(image, lang=self.language)
                    except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError, OSError) as exc:
                        raise OcrUnavailableError("Tesseract ou dados do idioma configurado indispon?veis.") from exc
                pages.append(PageOcr(index + 1, data))
            return DocumentOcr(tuple(pages))
        finally:
            document.close()
