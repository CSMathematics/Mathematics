#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path

from _common import EXAMCRITIC_DIR, REPO_ROOT, WORKSPACE_DIR, load_json, write_json


def metadata_path_from_arg(value: str) -> Path:
    path = Path(value)
    if path.suffix == ".json" or path.exists():
        return path if path.is_absolute() else REPO_ROOT / path
    return WORKSPACE_DIR / "topics" / f"{value}.metadata.json"


def unique(values: list[str]) -> list[str]:
    return sorted(set(values))


def build_evaluation(metadata: dict, evaluator: str) -> dict:
    template = load_json(EXAMCRITIC_DIR / "templates" / "evaluation-record.json")
    evaluation = copy.deepcopy(template)
    now = datetime.now(timezone.utc).isoformat()

    branches: list[str] = []
    question_types: list[str] = []
    for subquestion in metadata.get("subquestions", []):
        branches.extend(subquestion.get("branches", []))
        question_types.extend(subquestion.get("question_types", []))

    topic_id = metadata["topic_id"]
    evaluation.update(
        {
            "evaluation_id": f"eval-{topic_id}",
            "topic_id": topic_id,
            "created_at": now,
            "updated_at": now,
        }
    )
    evaluation["evaluator"]["name"] = evaluator
    evaluation["source"]["topic_tex_path"] = metadata.get("source_tex_path", "")
    evaluation["source"]["solution_tex_path"] = metadata.get("solution_tex_path", "")
    evaluation["taxonomy"]["branches"] = unique(branches)
    evaluation["taxonomy"]["question_types"] = unique(question_types)

    return evaluation


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a draft ExamCritic evaluation JSON.")
    parser.add_argument("topic_or_metadata", help="Topic id like G-001 or metadata JSON path")
    parser.add_argument("--evaluator", default="", help="Evaluator name or initials")
    parser.add_argument("--out-dir", default=str(WORKSPACE_DIR / "evaluations"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    metadata_path = metadata_path_from_arg(args.topic_or_metadata)
    if not metadata_path.exists():
        raise FileNotFoundError(metadata_path)

    metadata = load_json(metadata_path)
    evaluation = build_evaluation(metadata, args.evaluator)

    output_dir = Path(args.out_dir)
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir
    output_file = output_dir / f"{evaluation['evaluation_id']}.json"

    if output_file.exists() and not args.overwrite:
        raise FileExistsError(f"{output_file} exists. Use --overwrite.")

    write_json(output_file, evaluation)
    print(f"Wrote {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

