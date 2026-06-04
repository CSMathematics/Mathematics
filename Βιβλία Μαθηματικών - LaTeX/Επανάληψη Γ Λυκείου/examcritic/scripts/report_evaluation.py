#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _common import REPO_ROOT, WORKSPACE_DIR, load_json, write_text


MAX_SCORES = {
    "K1": 15,
    "K2": 10,
    "K3": 10,
    "K4": 20,
    "K5": 15,
    "K6": 20,
    "K7": 10,
}

CRITERION_LABELS = {
    "K1": "Μαθηματική αρτιότητα",
    "K2": "Σαφήνεια διατύπωσης",
    "K3": "Δομική ακεραιότητα",
    "K4": "Κάλυψη ύλης",
    "K5": "Βαθμός δυσκολίας",
    "K6": "Διδακτική αξία",
    "K7": "Χρονική εφικτότητα",
}


def format_value(value: object) -> str:
    if value is None or value == "":
        return "Δεν έχει συμπληρωθεί"
    return str(value)


def bullet_list(values: list[str]) -> str:
    if not values:
        return "- Δεν έχει συμπληρωθεί\n"
    return "".join(f"- {value}\n" for value in values)


def build_report(evaluation: dict) -> str:
    topic_id = evaluation.get("topic_id", "")
    lines: list[str] = [
        f"# ExamCritic Report: {topic_id}",
        "",
        "## Summary",
        "",
        f"- Preset: `{evaluation.get('preset_id', '')}`",
        f"- Status: `{evaluation.get('status', '')}`",
        f"- Final score: {format_value(evaluation.get('final_score'))}",
        f"- Score label: {format_value(evaluation.get('score_label'))}",
        f"- Topic source: `{evaluation.get('source', {}).get('topic_tex_path', '')}`",
        f"- Solution source: `{evaluation.get('source', {}).get('solution_tex_path', '')}`",
        "",
        "## Criterion Breakdown",
        "",
        "| Criterion | Label | Score | Max |",
        "| --- | --- | ---: | ---: |",
    ]

    for criterion, max_score in MAX_SCORES.items():
        total = evaluation.get("scores", {}).get(criterion, {}).get("total")
        score_text = "" if total is None else str(total)
        lines.append(f"| {criterion} | {CRITERION_LABELS[criterion]} | {score_text} | {max_score} |")

    taxonomy = evaluation.get("taxonomy", {})
    difficulty = evaluation.get("difficulty", {})
    time = evaluation.get("time", {})
    notes = evaluation.get("notes", {})
    automation = evaluation.get("automation")

    if automation:
        lines.extend(
            [
                "",
                "## Automation",
                "",
                f"- Mode: `{automation.get('mode', '')}`",
                f"- Requires teacher review: {automation.get('requires_teacher_review', False)}",
                f"- Review fields: {', '.join(automation.get('review_fields', []))}",
            ]
        )
        confidence = automation.get("confidence", {})
        if confidence:
            lines.append(f"- Confidence: {', '.join(f'{key}={value}' for key, value in confidence.items())}")

    lines.extend(
        [
            "",
            "## Taxonomy",
            "",
            f"- Branches: {', '.join(taxonomy.get('branches', [])) or 'Δεν έχει συμπληρωθεί'}",
            f"- Question types: {', '.join(taxonomy.get('question_types', [])) or 'Δεν έχει συμπληρωθεί'}",
            f"- Rare question types: {', '.join(taxonomy.get('rare_question_types', [])) or 'Δεν έχει συμπληρωθεί'}",
            f"- Monothematicity score: {format_value(taxonomy.get('monothematicity_score'))}",
            "",
            "## Difficulty And Time",
            "",
            f"- Raw difficulty: {format_value(difficulty.get('raw_difficulty'))}",
            f"- Technical complexity: {format_value(difficulty.get('technical_complexity'))}",
            f"- Conceptual depth: {format_value(difficulty.get('conceptual_depth'))}",
            f"- Solution steps: {format_value(difficulty.get('solution_steps'))}",
            f"- Originality: {format_value(difficulty.get('originality'))}",
            f"- Estimated time: {format_value(time.get('estimated_minutes'))}",
            "",
            "## Strengths",
            "",
            bullet_list(notes.get("strengths", [])),
            "## Issues",
            "",
            bullet_list(notes.get("issues", [])),
            "## Improvement Suggestions",
            "",
            bullet_list(notes.get("improvement_suggestions", [])),
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Markdown report from an evaluation JSON.")
    parser.add_argument("evaluation_json")
    parser.add_argument("--out-dir", default=str(WORKSPACE_DIR / "reports"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    evaluation_path = Path(args.evaluation_json)
    if not evaluation_path.is_absolute():
        evaluation_path = REPO_ROOT / evaluation_path

    evaluation = load_json(evaluation_path)
    output_dir = Path(args.out_dir)
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir
    output_file = output_dir / f"{evaluation['topic_id']}-report.md"

    if output_file.exists() and not args.overwrite:
        raise FileExistsError(f"{output_file} exists. Use --overwrite.")

    write_text(output_file, build_report(evaluation))
    print(f"Wrote {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
