from itertools import pairwise

import pytest

from src.chunking import chunk_documents
from src.chunking.splitter import split_text
from src.ingestion import Document

PARAGRAPHS = "\n\n".join(f"Paragraphe {i} " + "mot " * 10 for i in range(30))


def make_doc(page, text, source="cours.pdf", subject="Réseaux"):
    return Document(
        text=text,
        metadata={
            "source": source,
            "page": page,
            "total_pages": 10,
            "subject": subject,
            "doc_id": f"{source}:p{page}",
        },
    )


# --- splitter ---------------------------------------------------------------


def test_short_text_is_single_chunk():
    text = "Bonjour le monde"
    assert split_text(text, 800, 100) == [(0, len(text))]


def test_empty_text_gives_no_chunk():
    assert split_text("", 100, 10) == []


def test_chunks_never_exceed_size():
    text = "Phrase numéro un. " * 200
    assert all(end - start <= 200 for start, end in split_text(text, 200, 20))


def test_chunks_cover_whole_text_without_gaps():
    text = "Phrase numéro un. " * 200
    spans = split_text(text, 200, 20)
    assert spans[0][0] == 0
    assert spans[-1][1] == len(text)
    assert all(b[0] <= a[1] for a, b in pairwise(spans))


def test_overlap_is_applied():
    spans = split_text(PARAGRAPHS, 200, 60)
    assert any(b[0] < a[1] for a, b in pairwise(spans))


def test_no_overlap_when_zero():
    spans = split_text(PARAGRAPHS, 200, 0)
    assert all(b[0] == a[1] for a, b in pairwise(spans))


def test_text_without_separator_is_hard_cut():
    spans = split_text("a" * 1000, 300, 50)
    assert all(end - start <= 300 for start, end in spans)
    assert spans[-1][1] == 1000


def test_invalid_parameters_raise():
    with pytest.raises(ValueError):
        split_text("texte", 100, 100)
    with pytest.raises(ValueError):
        split_text("texte", 0, 0)


# --- chunker ----------------------------------------------------------------


def test_short_pages_are_merged():
    docs = [make_doc(i, f"Page {i} " + "mot " * 10) for i in range(1, 6)]
    chunks = chunk_documents(docs, 800, 100)
    assert len(chunks) == 1
    assert chunks[0].metadata["page_start"] == 1
    assert chunks[0].metadata["page_end"] == 5
    assert chunks[0].citation == "[cours.pdf, p.1-5]"


def test_long_page_is_split():
    text = " ".join(f"Phrase {i}." for i in range(300))
    chunks = chunk_documents([make_doc(1, text)], 800, 100)
    assert len(chunks) > 1
    assert all(len(c.text) <= 800 for c in chunks)
    assert all(c.metadata["page_start"] == c.metadata["page_end"] == 1 for c in chunks)


def test_chunks_never_mix_sources():
    docs = [
        make_doc(1, "alpha " * 50, source="a.pdf"),
        make_doc(1, "beta " * 50, source="b.pdf"),
    ]
    chunks = chunk_documents(docs, 800, 100)
    assert {c.metadata["source"] for c in chunks} == {"a.pdf", "b.pdf"}
    for chunk in chunks:
        other = "beta" if chunk.metadata["source"] == "a.pdf" else "alpha"
        assert other not in chunk.text


def test_metadata_is_complete():
    docs = [make_doc(3, "Contenu du cours sur le protocole TCP.")]
    chunk = chunk_documents(docs, 800, 100)[0]
    expected = {
        "source",
        "subject",
        "page_start",
        "page_end",
        "total_pages",
        "chunk_index",
        "chunk_id",
    }
    assert expected <= set(chunk.metadata)
    assert chunk.metadata["chunk_id"] == "cours:c0000"
    assert chunk.metadata["page_start"] == 3


def test_ids_are_unique_and_deterministic():
    docs = [make_doc(i, f"P{i} " + "mot " * 125) for i in range(1, 4)]
    first = [c.metadata["chunk_id"] for c in chunk_documents(docs, 800, 100)]
    second = [c.metadata["chunk_id"] for c in chunk_documents(docs, 800, 100)]
    assert first == second
    assert len(set(first)) == len(first)


def test_pages_are_tracked_across_the_document():
    docs = [make_doc(i, f"P{i} " + "mot " * 125) for i in range(1, 4)]
    chunks = chunk_documents(docs, 800, 100)
    assert chunks[0].metadata["page_start"] == 1
    assert chunks[-1].metadata["page_end"] == 3


def test_unsorted_pages_are_reordered():
    docs = [make_doc(i, f"Page {i} " + "mot " * 10) for i in range(5, 0, -1)]
    chunks = chunk_documents(docs, 800, 100)
    assert chunks[0].text.startswith("Page 1")


def test_no_documents_gives_no_chunks():
    assert chunk_documents([], 800, 100) == []
