import re
import unicodedata
from collections import Counter

_PAGE_NUMBER = re.compile(r"^\s*(?:page\s*)?\d{1,4}(?:\s*/\s*\d{1,4})?\s*$", re.IGNORECASE)


def normalize_text(text: str) -> str:
    """Normalise l'unicode, recolle les césures, compacte les espaces."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\x00", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # "informa-\ntique" -> "informatique"
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def find_repeated_lines(
    pages: list[str], min_pages: int = 4, ratio: float = 0.5, max_len: int = 120
) -> set[str]:
    """Repère les lignes qui reviennent sur au moins `ratio` des pages (en-têtes, pieds de page)."""
    if len(pages) < min_pages:
        return set()
    counter: Counter[str] = Counter()
    for page in pages:
        counter.update({ln.strip() for ln in page.splitlines() if ln.strip()})
    threshold = max(2, int(len(pages) * ratio))
    return {ln for ln, n in counter.items() if n >= threshold and len(ln) <= max_len}


def remove_lines(text: str, to_remove: set[str]) -> str:
    """Retire les lignes répétées et les numéros de page isolés."""
    kept = [
        ln for ln in text.splitlines() if ln.strip() not in to_remove and not _PAGE_NUMBER.match(ln)
    ]
    return "\n".join(kept).strip()
