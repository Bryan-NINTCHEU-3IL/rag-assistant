from pathlib import Path

SUBJECTS = {
    "reseau": "Réseaux",
    "droit": "Droit",
    "comptabilite": "Comptabilité",
    "marketing": "Marketing",
    "os": "Systèmes d'exploitation",
    "miniprojet": "Architecture sécurisée",
    "rgpd": "RGPD",
    "ds": "Examens",
}


def infer_subject(filename: str) -> str:
    """Déduit la matière du préfixe du nom de fichier (ex. reseau_cours.pdf)."""
    prefix = Path(filename).stem.split("_")[0].lower()
    return SUBJECTS.get(prefix, "Autre")
