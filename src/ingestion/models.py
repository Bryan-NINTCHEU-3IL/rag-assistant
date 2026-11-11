from dataclasses import dataclass, field


@dataclass
class Document:
    """Une page de cours, avec ses métadonnées."""

    text: str
    metadata: dict = field(default_factory=dict)
