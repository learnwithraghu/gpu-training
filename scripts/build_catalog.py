#!/usr/bin/env python3
"""Generate catalog.json from phase lesson folders."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASES_DIR = ROOT / "phases"
CATALOG_PATH = ROOT / "catalog.json"


def parse_front_matter(md_text: str) -> dict:
    if not md_text.startswith("---\n"):
        return {}
    parts = md_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    front_matter = parts[0].removeprefix("---\n")
    data: dict[str, object] = {}
    for line in front_matter.splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        value = raw.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
        data[key] = value
    return data


def lesson_sort_key(path: Path) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", path.name)
    index = int(match.group(1)) if match else 999
    return index, path.name


def phase_sort_key(path: Path) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", path.name)
    index = int(match.group(1)) if match else 999
    return index, path.name


def build_catalog() -> dict:
    phases = []
    for phase_dir in sorted(PHASES_DIR.iterdir(), key=phase_sort_key):
        if not phase_dir.is_dir():
            continue
        if phase_dir.name == "README.md":
            continue
        lessons = []
        for lesson_dir in sorted(phase_dir.iterdir(), key=lesson_sort_key):
            if not lesson_dir.is_dir():
                continue
            doc_path = lesson_dir / "docs" / "en.md"
            if not doc_path.exists():
                continue
            text = doc_path.read_text(encoding="utf-8")
            front = parse_front_matter(text)
            lessons.append(
                {
                    "id": f"{phase_dir.name}/{lesson_dir.name}",
                    "slug": lesson_dir.name,
                    "title": front.get("title", lesson_dir.name),
                    "type": front.get("type", "Learn"),
                    "duration_minutes": int(front.get("duration_minutes", 0) or 0),
                    "runtime": front.get("runtime", "Google Colab"),
                    "colab_url": front.get("colab_url", ""),
                    "doc_path": str(doc_path.relative_to(ROOT)),
                    "notebook_path": str((lesson_dir / "notebook" / "main.ipynb").relative_to(ROOT))
                    if (lesson_dir / "notebook" / "main.ipynb").exists()
                    else "",
                    "outputs_path": str((lesson_dir / "outputs").relative_to(ROOT)),
                }
            )
        phases.append(
            {
                "id": phase_dir.name,
                "title": phase_dir.name.replace("-", " ").title(),
                "path": str(phase_dir.relative_to(ROOT)),
                "lessons": lessons,
                "lesson_count": len(lessons),
            }
        )
    return {
        "name": "GPU Engineering From Scratch (Colab First)",
        "runtime_policy": "colab_only",
        "phase_count": len(phases),
        "phases": phases,
    }


def main() -> None:
    catalog = build_catalog()
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {CATALOG_PATH} with {catalog['phase_count']} phases.")


if __name__ == "__main__":
    main()
