#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _common import REPO_ROOT, WORKSPACE_DIR, read_text, repo_relative, resolve_from_repo, write_json


LETTER_TO_SLUG = {
    "Α": "A",
    "A": "A",
    "Β": "B",
    "B": "B",
    "Γ": "G",
    "G": "G",
    "C": "G",
    "Δ": "D",
    "D": "D",
}

SLUG_TO_FOLDER = {
    "A": "Α",
    "B": "Β",
    "G": "Γ",
    "D": "Δ",
}

SUBQUESTION_IDS = ["a", "b", "c", "d", "e", "f", "g", "h"]


def derive_topic_id(path: Path, topic_letter: str | None, explicit: str | None) -> str:
    if explicit:
        return explicit

    match = re.search(r"thema_([A-ZΑ-Ω])_(\d+)\.tex$", path.name)
    if match:
        slug = LETTER_TO_SLUG.get(match.group(1), match.group(1))
        return f"{slug}-{int(match.group(2)):03d}"

    if topic_letter:
        slug = LETTER_TO_SLUG.get(topic_letter, topic_letter)
        return f"{slug}-000"

    raise ValueError("Could not derive topic id. Use --topic-id.")


def auto_solution_path(topic_id: str) -> Path | None:
    match = re.fullmatch(r"([A-Z])-(\d{3})", topic_id)
    if not match:
        return None

    slug, number = match.groups()
    folder = SLUG_TO_FOLDER.get(slug)
    if not folder:
        return None

    candidate = REPO_ROOT / "Λύσεις θεμάτων" / folder / f"solution_{slug}_{int(number):02d}.tex"
    return candidate if candidate.exists() else None


def split_subquestions(block: str) -> list[str]:
    item_matches = list(re.finditer(r"(?m)^\s*\\item(?:\[[^\]]*\])?\s*", block))
    if not item_matches:
        stripped = block.strip()
        return [stripped] if stripped else []

    items: list[str] = []
    for index, match in enumerate(item_matches):
        start = match.end()
        end = item_matches[index + 1].start() if index + 1 < len(item_matches) else len(block)
        item = block[start:end].strip()
        if item:
            items.append(item)
    return items


def parse_topic(text: str) -> tuple[str, str, list[str], str, list[str]]:
    warnings: list[str] = []
    begin_match = re.search(r"\\begin\{thema\}\{([^}]*)\}", text)
    if not begin_match:
        raise ValueError("Unsupported file: missing \\begin{thema}{Γ}.")

    topic_letter = begin_match.group(1).strip()
    if topic_letter != "Γ":
        warnings.append(f"Expected Θέμα Γ, found Θέμα {topic_letter}.")

    end_match = re.search(r"\\end\{thema\}", text[begin_match.end() :])
    if not end_match:
        raise ValueError("Unsupported file: missing \\end{thema}.")

    end_start = begin_match.end() + end_match.start()
    end_end = begin_match.end() + end_match.end()
    body = text[begin_match.end() : end_start].strip()
    statement_raw = text[begin_match.start() : end_end].strip()

    erwthma_match = re.search(r"\\begin\{erwthma\}(.*?)\\end\{erwthma\}", body, flags=re.DOTALL)
    if not erwthma_match:
        warnings.append("Missing \\begin{erwthma}; using the whole body as one block.")
        return topic_letter, statement_raw, [body], "", warnings

    intro_text = body[: erwthma_match.start()].strip()
    subquestion_block = erwthma_match.group(1)
    subquestions = split_subquestions(subquestion_block)

    if not subquestions:
        warnings.append("No \\item entries found inside erwthma.")

    return topic_letter, statement_raw, subquestions, intro_text, warnings


def latex_features(text: str) -> dict[str, int | bool]:
    inline_math_count = len(re.findall(r"(?<!\\)\$(?!\$)", text)) // 2
    inline_math_count += len(re.findall(r"\\\(", text))

    display_math_count = len(re.findall(r"\\\[", text))
    display_math_count += len(re.findall(r"(?<!\\)\$\$", text)) // 2
    display_math_count += len(
        re.findall(r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}", text)
    )

    return {
        "inline_math_count": inline_math_count,
        "display_math_count": display_math_count,
        "tikz_or_pgfplots": "tikzpicture" in text or "\\begin{axis}" in text,
        "tables": "\\begin{tabular}" in text or "tkzTab" in text,
    }


def build_metadata(topic_path: Path, solution_path: Path | None, topic_id: str | None) -> dict:
    text = read_text(topic_path)
    topic_letter, statement_raw, subquestions, intro_text, warnings = parse_topic(text)
    resolved_topic_id = derive_topic_id(topic_path, topic_letter, topic_id)

    if solution_path is None:
        solution_path = auto_solution_path(resolved_topic_id)
    elif not solution_path.exists():
        warnings.append(f"Solution path does not exist: {solution_path}")

    metadata = {
        "schema": "examcritic.topic_metadata.v0",
        "topic_id": resolved_topic_id,
        "topic_letter": topic_letter,
        "source_tex_path": repo_relative(topic_path),
        "solution_tex_path": repo_relative(solution_path) if solution_path else "",
        "statement_raw": statement_raw,
        "intro_text": intro_text,
        "subquestions": [],
        "subquestion_count": len(subquestions),
        "latex_features": latex_features(statement_raw),
        "parse_warnings": warnings,
    }

    for index, subquestion in enumerate(subquestions):
        metadata["subquestions"].append(
            {
                "id": SUBQUESTION_IDS[index] if index < len(SUBQUESTION_IDS) else str(index + 1),
                "text_raw": subquestion,
                "question_types": [],
                "branches": [],
            }
        )

    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse a Θέμα Γ .tex file into ExamCritic metadata.")
    parser.add_argument("topic_tex", help="Path to Θέματα/Γ/thema_G_XX.tex")
    parser.add_argument("--solution", help="Optional path to matching solution .tex")
    parser.add_argument("--topic-id", help="Override topic id, e.g. G-001")
    parser.add_argument("--out-dir", default=str(WORKSPACE_DIR / "topics"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    topic_path = resolve_from_repo(args.topic_tex)
    if not topic_path.exists():
        raise FileNotFoundError(topic_path)

    solution_path = resolve_from_repo(args.solution) if args.solution else None
    metadata = build_metadata(topic_path, solution_path, args.topic_id)

    output_path = Path(args.out_dir)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_file = output_path / f"{metadata['topic_id']}.metadata.json"

    if output_file.exists() and not args.overwrite:
        raise FileExistsError(f"{output_file} exists. Use --overwrite.")

    write_json(output_file, metadata)
    print(f"Wrote {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

