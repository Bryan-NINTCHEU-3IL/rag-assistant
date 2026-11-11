from collections import defaultdict
from pathlib import Path

from src.config import settings
from src.ingestion import Document

from .models import Chunk
from .splitter import split_text

PAGE_SEPARATOR = "\n\n"


def _chunk_source(source: str, pages: list[Document], chunk_size: int, overlap: int) -> list[Chunk]:
    """Découpe un cours entier en conservant les pages couvertes par chaque chunk."""
    pages = sorted(pages, key=lambda d: d.metadata["page"])

    ranges: list[tuple[int, int, int]] = []  # (début, fin, numéro de page)
    cursor = 0
    for doc in pages:
        ranges.append((cursor, cursor + len(doc.text), doc.metadata["page"]))
        cursor += len(doc.text) + len(PAGE_SEPARATOR)
    full_text = PAGE_SEPARATOR.join(doc.text for doc in pages)

    first = pages[0].metadata
    stem = Path(source).stem
    chunks: list[Chunk] = []
    for start, end in split_text(full_text, chunk_size, overlap):
        raw = full_text[start:end]
        text = raw.strip()
        if not text:
            continue
        start += len(raw) - len(raw.lstrip())
        end = start + len(text)
        covered = [page for p_start, p_end, page in ranges if p_start < end and p_end > start]
        index = len(chunks)
        chunks.append(
            Chunk(
                text=text,
                metadata={
                    "source": source,
                    "subject": first.get("subject", "Autre"),
                    "page_start": covered[0],
                    "page_end": covered[-1],
                    "total_pages": first.get("total_pages", len(pages)),
                    "chunk_index": index,
                    "chunk_id": f"{stem}:c{index:04d}",
                },
            )
        )
    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """Transforme les pages en chunks, cours par cours."""
    chunk_size = settings.chunk_size if chunk_size is None else chunk_size
    overlap = settings.chunk_overlap if overlap is None else overlap

    by_source: dict[str, list[Document]] = defaultdict(list)
    for doc in documents:
        by_source[doc.metadata["source"]].append(doc)

    chunks: list[Chunk] = []
    for source, pages in by_source.items():
        chunks.extend(_chunk_source(source, pages, chunk_size, overlap))
    return chunks
