#!/usr/bin/env python3
"""Generate catalog.json from phase lesson folders."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASES_DIR = ROOT / "phases"
CATALOG_PATH = ROOT / "catalog.json"


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        return [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
    if value.isdigit():
        return int(value)
    return value


def parse_front_matter(md_text: str) -> dict:
    if not md_text.startswith("---\n"):
        return {}
    parts = md_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    front_matter = parts[0].removeprefix("---\n")
    data: dict[str, object] = {}
    lines = front_matter.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if ":" not in line:
            idx += 1
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        value = raw.strip()
        if not value:
            items: list[str] = []
            look_ahead = idx + 1
            while look_ahead < len(lines) and lines[look_ahead].startswith("  - "):
                items.append(str(parse_scalar(lines[look_ahead][4:].strip())))
                look_ahead += 1
            if items:
                data[key] = items
                idx = look_ahead
                continue
            data[key] = ""
            idx += 1
            continue
        data[key] = parse_scalar(value)
        idx += 1
    return data


def lesson_sort_key(path: Path) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", path.name)
    index = int(match.group(1)) if match else 999
    return index, path.name


def phase_sort_key(path: Path) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", path.name)
    index = int(match.group(1)) if match else 999
    return index, path.name


def infer_role_tags(phase_id: str) -> list[str]:
    mapping = {
        "03-gpus-for-data-science": ["data-science"],
        "04-gpus-for-data-engineering": ["data-engineering"],
        "05-gpus-for-devops-mlops": ["devops"],
        "07-capstone-projects-by-role": ["devops", "data-science", "data-engineering"],
    }
    return mapping.get(phase_id, [])


def infer_artifact_type(path: Path) -> str:
    normalized = path.stem.lower().replace("_", "-")
    if "checklist" in normalized:
        return "checklist"
    if "benchmark" in normalized:
        return "benchmark-summary"
    if "runbook" in normalized:
        return "runbook"
    if "guide" in normalized or "troubleshoot" in normalized:
        return "troubleshooting-guide"
    return "artifact"


def collect_output_artifacts(outputs_dir: Path) -> list[dict[str, str]]:
    if not outputs_dir.exists():
        return []
    artifacts: list[dict[str, str]] = []
    for artifact in sorted(outputs_dir.rglob("*")):
        if not artifact.is_file():
            continue
        artifacts.append(
            {
                "name": artifact.stem.replace("-", " ").replace("_", " ").title(),
                "path": str(artifact.relative_to(ROOT)),
                "type": infer_artifact_type(artifact),
            }
        )
    return artifacts


def compute_lesson_status(doc_exists: bool, notebook_exists: bool, colab_url: str) -> str:
    if doc_exists and notebook_exists and colab_url.startswith("https://colab.research.google.com/"):
        return "runnable"
    if doc_exists:
        return "documented"
    return "planned"


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
            notebook_path = lesson_dir / "notebook" / "main.ipynb"
            outputs_dir = lesson_dir / "outputs"

            front: dict[str, object] = {}
            if doc_path.exists():
                text = doc_path.read_text(encoding="utf-8")
                front = parse_front_matter(text)

            colab_url = str(front.get("colab_url", ""))
            lesson_status = compute_lesson_status(doc_path.exists(), notebook_path.exists(), colab_url)
            lesson_type = str(front.get("type", "Learn"))
            roles = front.get("roles", infer_role_tags(phase_dir.name))
            if not isinstance(roles, list):
                roles = [str(roles)] if roles else []

            prerequisites = front.get("prerequisites", [])
            if not isinstance(prerequisites, list):
                prerequisites = [str(prerequisites)] if prerequisites else []

            objectives = front.get("objectives", [])
            if not isinstance(objectives, list):
                objectives = [str(objectives)] if objectives else []

            lessons.append(
                {
                    "id": f"{phase_dir.name}/{lesson_dir.name}",
                    "slug": lesson_dir.name,
                    "title": front.get("title", lesson_dir.name.replace("-", " ").title()),
                    "type": lesson_type,
                    "status": lesson_status,
                    "duration_minutes": int(front.get("duration_minutes", 0) or 0),
                    "runtime": front.get("runtime", "Google Colab"),
                    "colab_url": colab_url,
                    "doc_path": str(doc_path.relative_to(ROOT)),
                    "notebook_path": str(notebook_path.relative_to(ROOT)) if notebook_path.exists() else "",
                    "outputs_path": str(outputs_dir.relative_to(ROOT)),
                    "artifacts": collect_output_artifacts(outputs_dir),
                    "roles": roles,
                    "prerequisites": prerequisites,
                    "objectives": objectives,
                }
            )
        runnable_count = sum(1 for lesson in lessons if lesson["status"] == "runnable")
        documented_count = sum(1 for lesson in lessons if lesson["status"] == "documented")
        phase_status = "planned"
        if runnable_count > 0:
            phase_status = "runnable"
        elif documented_count > 0:
            phase_status = "documented"
        phases.append(
            {
                "id": phase_dir.name,
                "title": phase_dir.name.replace("-", " ").title(),
                "path": str(phase_dir.relative_to(ROOT)),
                "lessons": lessons,
                "lesson_count": len(lessons),
                "status": phase_status,
                "runnable_count": runnable_count,
                "documented_count": documented_count,
            }
        )
    total_lessons = sum(int(phase["lesson_count"]) for phase in phases)
    total_runnable = sum(int(phase["runnable_count"]) for phase in phases)
    total_documented = sum(int(phase["documented_count"]) for phase in phases)
    return {
        "name": "GPU Engineering From Scratch (Colab First)",
        "runtime_policy": "colab_only",
        "phase_count": len(phases),
        "lesson_count": total_lessons,
        "runnable_count": total_runnable,
        "documented_count": total_documented,
        "phases": phases,
    }


def main() -> None:
    catalog = build_catalog()
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {CATALOG_PATH} with {catalog['phase_count']} phases.")


if __name__ == "__main__":
    main()
