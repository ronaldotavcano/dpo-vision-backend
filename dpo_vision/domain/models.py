from dataclasses import dataclass


@dataclass(frozen=True)
class PageOcr:
    number: int
    data: str


@dataclass(frozen=True)
class DocumentOcr:
    pages: tuple[PageOcr, ...]

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
                columns = row.split("\t", 1)
                lines.append(f"{page.number}\t{columns[1]}" if len(columns) == 2 else row)
        return "\n".join(lines) + ("\n" if lines else "")
