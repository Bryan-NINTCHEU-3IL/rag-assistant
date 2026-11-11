from src.ingestion import load_directory, load_pdf
from src.ingestion.cleaning import find_repeated_lines, normalize_text, remove_lines
from src.ingestion.subjects import infer_subject


def test_normalize_fixes_hyphenation_and_spaces():
    assert normalize_text("informa-\ntique   et  droit") == "informatique et droit"


def test_find_repeated_lines():
    pages = [f"En-tête\ncontenu {i}" for i in range(6)]
    assert find_repeated_lines(pages) == {"En-tête"}


def test_find_repeated_lines_ignores_short_documents():
    assert find_repeated_lines(["En-tête\na", "En-tête\nb"]) == set()


def test_remove_lines_drops_page_numbers():
    assert remove_lines("texte\n12\nPage 3\nsuite", set()) == "texte\nsuite"


def test_infer_subject():
    assert infer_subject("reseau_cours.pdf") == "Réseaux"
    assert infer_subject("inconnu.pdf") == "Autre"


def test_load_pdf_one_document_per_page(sample_pdf):
    docs = load_pdf(sample_pdf)
    assert len(docs) == 5
    assert [d.metadata["page"] for d in docs] == [1, 2, 3, 4, 5]


def test_load_pdf_metadata(sample_pdf):
    meta = load_pdf(sample_pdf)[0].metadata
    assert meta["source"] == "reseau_test.pdf"
    assert meta["subject"] == "Réseaux"
    assert meta["total_pages"] == 5
    assert meta["doc_id"] == "reseau_test:p1"


def test_load_pdf_removes_header_and_page_number(sample_pdf):
    docs = load_pdf(sample_pdf)
    assert all("Licence 2" not in d.text for d in docs)
    assert all("TCP" in d.text for d in docs)


def test_blank_pdf_returns_empty(blank_pdf):
    assert load_pdf(blank_pdf) == []


def test_corrupt_pdf_does_not_crash(corrupt_pdf):
    assert load_pdf(corrupt_pdf) == []


def test_load_directory_skips_bad_files(tmp_path, sample_pdf, corrupt_pdf):
    # sample_pdf et corrupt_pdf sont déjà dans tmp_path
    docs = load_directory(tmp_path)
    assert len(docs) == 5
