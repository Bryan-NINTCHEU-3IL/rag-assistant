import logging
from pathlib import Path

from pypdf import PdfReader

from .cleaning import find_repeated_lines, normalize_text, remove_lines
from .models import Document
from .subjects import infer_subject

logger = logging.getLogger(__name__)

MIN_PAGE_CHARS = 20
LOW_DENSITY_THRESHOLD = 200  # caractères par page en moyenne


def _extract_page(page, index: int, filename: str) -> str:
    try:
        return normalize_text(page.extract_text() or "")
    except Exception as exc:
        logger.warning("%s p.%d : extraction impossible (%s)", filename, index, exc)
        return ""


def load_pdf(path: Path) -> list[Document]:
    """Charge un PDF et renvoie un Document par page exploitable.

    Ne lève jamais d'exception : un fichier illisible est logué et renvoie [].
    """
    path = Path(path)
    try:
        reader = PdfReader(path)
        raw_pages = [_extract_page(p, i, path.name) for i, p in enumerate(reader.pages, 1)]
    except Exception as exc:
        logger.error("%s : fichier illisible (%s)", path.name, exc)
        return []

    total = len(raw_pages)
    repeated = find_repeated_lines(raw_pages)
    subject = infer_subject(path.name)

    documents: list[Document] = []
    for number, raw in enumerate(raw_pages, 1):
        text = remove_lines(raw, repeated)
        if len(text) < MIN_PAGE_CHARS:
            continue
        documents.append(
            Document(
                text=text,
                metadata={
                    "source": path.name,
                    "page": number,
                    "total_pages": total,
                    "subject": subject,
                    "doc_id": f"{path.stem}:p{number}",
                },
            )
        )

    if not documents:
        logger.warning("%s : aucun texte extrait (PDF scanné ou images ?)", path.name)
    elif sum(len(d.text) for d in documents) / total < LOW_DENSITY_THRESHOLD:
        logger.warning("%s : faible densité de texte (diapositives ?)", path.name)
    return documents
