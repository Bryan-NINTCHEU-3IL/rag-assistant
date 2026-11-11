from dataclasses import dataclass, field


@dataclass
class Chunk:
    """Un morceau de cours prêt à être indexé."""

    text: str
    metadata: dict = field(default_factory=dict)

    @property
    def citation(self) -> str:
        meta = self.metadata
        start, end = meta["page_start"], meta["page_end"]
        pages = f"p.{start}" if start == end else f"p.{start}-{end}"
        return f"[{meta['source']}, {pages}]"
