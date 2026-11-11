import pytest
from pypdf import PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@pytest.fixture
def sample_pdf(tmp_path):
    """PDF de 5 pages avec en-tête et numéro de page répétés."""
    path = tmp_path / "reseau_test.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    for i in range(1, 6):
        c.drawString(72, 800, "Cours de réseaux - Licence 2")
        c.drawString(72, 700, f"Contenu unique de la page {i} sur le protocole TCP et les paquets.")
        c.drawString(72, 40, str(i))
        c.showPage()
    c.save()
    return path


@pytest.fixture
def blank_pdf(tmp_path):
    path = tmp_path / "vide.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture
def corrupt_pdf(tmp_path):
    path = tmp_path / "casse.pdf"
    path.write_bytes(b"ceci n'est pas un pdf")
    return path
