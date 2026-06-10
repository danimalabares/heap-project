from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GERBY = ROOT / "gerby"

# configuration for the website
COMMENTS = str(GERBY / "comments.sqlite")
DATABASE = str(GERBY / "stack.sqlite")
DOWNLOADS = str(GERBY / "downloads")
UNIT = "section"
DEPTH = 0

# configuration for the import
PATH = str(GERBY / "document")
PAUX = str(ROOT / "book.paux")
TAGS = str(GERBY / "tags")
PDF = str(ROOT / "book.pdf")
