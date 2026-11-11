import argparse
import logging
from pathlib import Path

from src.config import settings

from .pipeline import load_directory, summarize


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingestion des PDF de cours")
    parser.add_argument("--path", type=Path, default=settings.data_dir)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    documents = load_directory(args.path)
    stats = summarize(documents)

    print(f"\n{'Fichier':<45}{'Pages':>11}{'Caractères':>12}{'Car./page':>11}")
    for pdf in sorted(args.path.glob("*.pdf")):
        s = stats.get(pdf.name)
        if s is None:
            print(f"{pdf.name:<45}  AUCUN TEXTE EXTRAIT")
            continue
        pages = f"{s['kept']}/{s['total']}"
        print(f"{pdf.name:<45}{pages:>11}{s['chars']:>12}{s['chars'] // s['kept']:>11}")
    print(f"\nTotal : {len(documents)} pages, {sum(s['chars'] for s in stats.values())} caractères")


if __name__ == "__main__":
    main()
