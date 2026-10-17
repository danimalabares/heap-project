import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "scripts"))
from gerby_registry import check_runtime

check_runtime()

from gerby import app


application = app
