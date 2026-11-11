import logging
from pathlib import Path

from .models import Document
from .pdf_loader import load_pdf

logger = logging.getLogger(__name__)


def load_directory(directory: Path) -> list[Document]:
    """Charge tous les PDF d'un dossier."""
    directory = Path(directory)
    pdfs = sorted(directory.glob("*.pdf"))
    if not pdfs:
        logger.warning("Aucun PDF trouvé dans %s", directory)
    documents: list[Document] = []
    for pdf in pdfs:
        documents.extend(load_pdf(pdf))
    return documents


def summarize(documents: list[Document]) -> dict[str, dict]:
    """Statistiques par fichier : pages conservées, pages totales, caractères."""
    stats: dict[str, dict] = {}
    for doc in documents:
        s = stats.setdefault(
            doc.metadata["source"],
            {"kept": 0, "total": doc.metadata["total_pages"], "chars": 0},
        )
        s["kept"] += 1
        s["chars"] += len(doc.text)
    return stats
