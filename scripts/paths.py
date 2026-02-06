from pathlib import Path

# Project root = /workspace (because this file lives in /workspace/scripts)
ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
FRONTEND_DIR = ROOT / "frontend"
SCRIPTS_DIR = ROOT / "scripts"
TRANSCRIPTS_DIR = ROOT / "transcripts"


def p(*parts: str) -> Path:
    """
    Convenience helper: p("data", "file.csv") -> ROOT/data/file.csv
    """
    return ROOT.joinpath(*parts)
