import argparse
import logging
from collections import defaultdict
from pathlib import Path
from statistics import median

from src.config import settings
from src.ingestion import load_directory

from .chunker import chunk_documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Découpage des cours en chunks")
    parser.add_argument("--path", type=Path, default=settings.data_dir)
    parser.add_argument("--size", type=int, default=settings.chunk_size)
    parser.add_argument("--overlap", type=int, default=settings.chunk_overlap)
    parser.add_argument("--show", type=int, default=None, help="Affiche le chunk numéro N")
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    chunks = chunk_documents(load_directory(args.path), args.size, args.overlap)
    if not chunks:
        print("Aucun chunk produit.")
        return

    by_source: dict[str, list[int]] = defaultdict(list)
    by_subject: dict[str, int] = defaultdict(int)
    for chunk in chunks:
        by_source[chunk.metadata["source"]].append(len(chunk.text))
        by_subject[chunk.metadata["subject"]] += 1

    print(f"\nTaille {args.size}, chevauchement {args.overlap}")
    print(f"\n{'Fichier':<45}{'Chunks':>8}{'Moy. car.':>11}")
    for source, sizes in sorted(by_source.items()):
        print(f"{source:<45}{len(sizes):>8}{sum(sizes) // len(sizes):>11}")

    print(f"\n{'Matière':<30}{'Chunks':>8}{'Part':>8}")
    for subject, count in sorted(by_subject.items(), key=lambda kv: -kv[1]):
        print(f"{subject:<30}{count:>8}{count / len(chunks):>8.0%}")

    sizes = [len(c.text) for c in chunks]
    print(
        f"\nTotal : {len(chunks)} chunks | "
        f"min {min(sizes)}, médiane {int(median(sizes))}, max {max(sizes)} caractères"
    )

    if args.show is not None:
        chunk = chunks[args.show % len(chunks)]
        print(f"\n--- Chunk {chunk.metadata['chunk_id']} {chunk.citation} ---")
        print(chunk.text)


if __name__ == "__main__":
    main()
