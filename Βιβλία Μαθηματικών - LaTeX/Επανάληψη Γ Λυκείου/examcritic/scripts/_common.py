from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
EXAMCRITIC_DIR = SCRIPT_DIR.parent
REPO_ROOT = EXAMCRITIC_DIR.parent
WORKSPACE_DIR = EXAMCRITIC_DIR / "workspace"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_from_repo(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def score_label(score: float | None) -> str:
    if score is None:
        return ""
    if score >= 90:
        return "Εξαιρετικό"
    if score >= 75:
        return "Πολύ καλό"
    if score >= 60:
        return "Αποδεκτό"
    if score >= 40:
        return "Προβληματικό"
    return "Ακατάλληλο"


def load_active_preset(preset_id: str) -> dict[str, Any]:
    preset_file = EXAMCRITIC_DIR / "data" / "presets" / "panelladikes-g-lykeiou.json"
    data = load_json(preset_file)
    for preset in data["presets"]:
        if preset["id"] == preset_id:
            return preset
    raise ValueError(f"Preset not found: {preset_id}")

