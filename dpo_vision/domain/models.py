from dataclasses import dataclass
import csv
import io


@dataclass(frozen=True)
class PageOcr:
    number: int
    data: str


@dataclass(frozen=True)
class DocumentOcr:
    pages: tuple[PageOcr, ...]

    def words(self) -> list[dict]:
        """Return OCR words with pixel coordinates in their rendered page."""
        words = []
        for page in self.pages:
            rows = list(csv.DictReader(io.StringIO(page.data), delimiter="\t"))
            page_row = next((row for row in rows if row.get("level") == "1"), None)
            if page_row is None:
                continue
            width, height = int(page_row["width"]), int(page_row["height"])
            for row in rows:
                text = (row.get("text") or "").strip()
                if row.get("level") != "5" or not text:
                    continue
                words.append({
                    "id": len(words) + 1,
                    "texto": text,
                    "pagina": page.number,
                    "coordenadas": {
                        "x": int(row["left"]), "y": int(row["top"]),
                        "largura": int(row["width"]), "altura": int(row["height"]),
                    },
                    "pagina_largura": width,
                    "pagina_altura": height,
                })
        return words

    def as_tsv(self) -> str:
        """Combine Tesseract TSV output while retaining a single header."""
        lines = []
        for page in self.pages:
            rows = page.data.splitlines()
            if not rows:
                continue
            if not lines:
                lines.append(rows[0])
            for row in rows[1:]:
                columns = row.split("\t")
                if len(columns) > 1:
                    columns[1] = str(page.number)
                lines.append("\t".join(columns))
        return "\n".join(lines) + ("\n" if lines else "")
