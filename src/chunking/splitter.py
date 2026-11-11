SEPARATORS = ["\n\n", "\n", ". ", " "]


def _split_span(
    text: str, start: int, end: int, max_len: int, level: int = 0
) -> list[tuple[int, int]]:
    """Découpe text[start:end] en morceaux de max_len caractères au plus.

    Coupe d'abord aux paragraphes, puis aux lignes, aux phrases, aux mots,
    et enfin à longueur fixe. Les morceaux sont contigus.
    """
    if end - start <= max_len:
        return [(start, end)]
    if level >= len(SEPARATORS):
        return [(i, min(i + max_len, end)) for i in range(start, end, max_len)]

    sep = SEPARATORS[level]
    spans: list[tuple[int, int]] = []
    pos = start
    while pos < end:
        idx = text.find(sep, pos, end)
        piece_end = end if idx == -1 else idx + len(sep)
        spans.extend(_split_span(text, pos, piece_end, max_len, level + 1))
        pos = piece_end
    return spans


def _pack(spans: list[tuple[int, int]], max_len: int, overlap: int) -> list[tuple[int, int]]:
    """Assemble les morceaux en chunks de max_len caractères, avec chevauchement."""
    chunks: list[tuple[int, int]] = []
    current: list[tuple[int, int]] = []
    for span in spans:
        if current and span[1] - current[0][0] > max_len:
            chunks.append((current[0][0], current[-1][1]))
            kept: list[tuple[int, int]] = []
            total = 0
            for prev in reversed(current):
                length = prev[1] - prev[0]
                if total + length > overlap:
                    break
                kept.insert(0, prev)
                total += length
            current = kept
            while current and span[1] - current[0][0] > max_len:
                current.pop(0)
        current.append(span)
    if current:
        chunks.append((current[0][0], current[-1][1]))
    return chunks


def split_text(text: str, chunk_size: int, overlap: int) -> list[tuple[int, int]]:
    """Renvoie les positions (début, fin) des chunks dans `text`."""
    if chunk_size <= 0:
        raise ValueError("chunk_size doit être strictement positif")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap doit être compris entre 0 et chunk_size - 1")
    if not text:
        return []
    spans = _split_span(text, 0, len(text), chunk_size)
    return _pack(spans, chunk_size, overlap)
