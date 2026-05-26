#!/usr/bin/env python3
"""Validate lesson structure and key documentation links."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASES_DIR = ROOT / "phases"
URL_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


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
        value = raw.strip().strip('"')
        data[key] = value
    return data


def validate_markdown_links(path: Path, content: str) -> list[str]:
    errors = []
    for match in URL_RE.finditer(content):
        target = match.group(1).strip()
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue
        file_target = (path.parent / target).resolve()
        if not file_target.exists():
            errors.append(f"Broken relative link in {path}: {target}")
    return errors


def main() -> int:
    errors: list[str] = []

    for phase_dir in sorted(PHASES_DIR.iterdir()):
        if not phase_dir.is_dir():
            continue
        for lesson_dir in sorted(phase_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            doc_path = lesson_dir / "docs" / "en.md"
            if not doc_path.exists():
                errors.append(f"Missing docs/en.md: {lesson_dir}")
                continue

            doc_text = doc_path.read_text(encoding="utf-8")
            front = parse_front_matter(doc_text)
            lesson_type = str(front.get("type", "Learn"))
            colab_url = str(front.get("colab_url", ""))

            errors.extend(validate_markdown_links(doc_path, doc_text))

            if lesson_type in {"Build", "Project"}:
                notebook = lesson_dir / "notebook" / "main.ipynb"
                if not notebook.exists():
                    errors.append(f"Missing notebook/main.ipynb for {lesson_type} lesson: {lesson_dir}")
                if not colab_url.startswith("https://colab.research.google.com/"):
                    errors.append(f"Missing or invalid colab_url in front matter: {doc_path}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("Lesson validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
