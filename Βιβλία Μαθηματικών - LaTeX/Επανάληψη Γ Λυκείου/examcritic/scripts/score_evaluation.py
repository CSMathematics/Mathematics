#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import REPO_ROOT, clamp, load_active_preset, load_json, score_label, write_json


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def sum_indicators(evaluation: dict, criterion: str, missing: list[str]) -> float | None:
    indicators = evaluation["scores"][criterion].get("indicators", {})
    values = []
    for key, value in indicators.items():
        if is_number(value):
            values.append(float(value))
        else:
            missing.append(f"scores.{criterion}.indicators.{key}")

    if len(values) != len(indicators):
        return None
    return sum(values)


def compute_k3(evaluation: dict, missing: list[str]) -> float | None:
    indicators = evaluation["scores"]["K3"]["indicators"]
    required = ["K3.1", "K3.2", "K3.3"]
    if any(not is_number(indicators.get(key)) for key in required):
        for key in required:
            if not is_number(indicators.get(key)):
                missing.append(f"scores.K3.indicators.{key}")
        return None
    return 2 * indicators["K3.1"] + 2 * indicators["K3.2"] + indicators["K3.3"]


def compute_k4(evaluation: dict, missing: list[str]) -> float | None:
    indicators = evaluation["scores"]["K4"].get("indicators", {})
    if all(is_number(value) for value in indicators.values()):
        return sum(float(value) for value in indicators.values())

    taxonomy = evaluation.get("taxonomy", {})
    monothematicity = taxonomy.get("monothematicity_score")
    question_types = set(taxonomy.get("question_types", []))
    branches = set(taxonomy.get("branches", []))

    if not question_types:
        missing.append("taxonomy.question_types or scores.K4.indicators.K4.1")
    if not branches:
        missing.append("taxonomy.branches or scores.K4.indicators.K4.2")
    if not is_number(monothematicity):
        missing.append("taxonomy.monothematicity_score or scores.K4.indicators.K4.4")

    if missing and any(field.startswith("taxonomy.") for field in missing):
        return None

    rare_question_types = set(taxonomy.get("rare_question_types", []))

    k4_1 = min(len(question_types), 5)
    k4_2 = min(len(branches) * 2, 8)
    k4_3 = min(len(rare_question_types), 4)
    k4_4 = float(monothematicity)

    evaluation["scores"]["K4"]["indicators"] = {
        "K4.1": k4_1,
        "K4.2": k4_2,
        "K4.3": k4_3,
        "K4.4": k4_4,
    }
    return k4_1 + k4_2 + k4_3 + k4_4


def compute_raw_difficulty(evaluation: dict, missing: list[str]) -> float | None:
    difficulty = evaluation.get("difficulty", {})
    if is_number(difficulty.get("raw_difficulty")):
        return float(difficulty["raw_difficulty"])

    fields = ["technical_complexity", "conceptual_depth", "solution_steps", "originality"]
    if any(not is_number(difficulty.get(field)) for field in fields):
        for field in fields:
            if not is_number(difficulty.get(field)):
                missing.append(f"difficulty.{field}")
        return None

    raw = (
        2 * difficulty["technical_complexity"]
        + 2 * difficulty["conceptual_depth"]
        + difficulty["solution_steps"]
        + difficulty["originality"]
    ) / 6
    difficulty["raw_difficulty"] = round(raw, 2)
    return raw


def compute_k5(evaluation: dict, preset: dict, missing: list[str]) -> float | None:
    raw = compute_raw_difficulty(evaluation, missing)
    if raw is None:
        return None

    target_min = preset["target_difficulty"]["min"]
    target_max = preset["target_difficulty"]["max"]
    if target_min <= raw <= target_max:
        return 15.0

    distance = min(abs(raw - target_min), abs(raw - target_max))
    return clamp(15 - 3 * distance, 0, 15)


def compute_k7(evaluation: dict, preset: dict, missing: list[str]) -> float | None:
    estimated = evaluation.get("time", {}).get("estimated_minutes")
    if not is_number(estimated):
        missing.append("time.estimated_minutes")
        return None

    band = preset["full_time_band_minutes"]
    if band["min"] <= estimated <= band["max"]:
        return 10.0

    nearest = band["min"] if estimated < band["min"] else band["max"]
    distance_ratio = abs(estimated - nearest) / preset["target_time_minutes"]
    return clamp(10 - 20 * distance_ratio, 0, 10)


def compute_scores(evaluation: dict, preset: dict) -> tuple[dict[str, float], list[str]]:
    missing: list[str] = []
    scores: dict[str, float] = {}

    for criterion in ["K1", "K2", "K6"]:
        existing = evaluation["scores"][criterion].get("total")
        scores[criterion] = float(existing) if is_number(existing) else sum_indicators(
            evaluation, criterion, missing
        )

    existing_k3 = evaluation["scores"]["K3"].get("total")
    scores["K3"] = float(existing_k3) if is_number(existing_k3) else compute_k3(evaluation, missing)

    existing_k4 = evaluation["scores"]["K4"].get("total")
    scores["K4"] = float(existing_k4) if is_number(existing_k4) else compute_k4(evaluation, missing)

    scores["K5"] = compute_k5(evaluation, preset, missing)
    scores["K7"] = compute_k7(evaluation, preset, missing)

    complete_scores = {key: value for key, value in scores.items() if value is not None}
    return complete_scores, missing


def normalized_weights(preset: dict) -> dict[str, float]:
    effective = {
        key: preset["base_weights"][key] * preset["multipliers"].get(key, 1)
        for key in preset["base_weights"]
    }
    total = sum(effective.values())
    return {key: 100 * value / total for key, value in effective.items()}


def decide_status(evaluation: dict, preset: dict, final_score: float, scores: dict[str, float]) -> str:
    rules = preset["approval_rules"]
    if evaluation.get("critical_issues"):
        return "review"
    if scores["K1"] < rules["minimum_K1_score"]:
        return "review"
    if final_score >= rules["minimum_final_score"]:
        return "approved"
    if final_score >= 60:
        return "review"
    return "reject_for_now"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a completed ExamCritic evaluation JSON.")
    parser.add_argument("evaluation_json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    evaluation_path = Path(args.evaluation_json)
    if not evaluation_path.is_absolute():
        evaluation_path = REPO_ROOT / evaluation_path

    evaluation = load_json(evaluation_path)
    preset = load_active_preset(evaluation["preset_id"])
    scores, missing = compute_scores(evaluation, preset)

    if missing:
        print("Incomplete evaluation. Fill these fields first:")
        for field in sorted(set(missing)):
            print(f"- {field}")
        return 2

    weights = normalized_weights(preset)
    final_score = 0.0
    for criterion, raw_score in scores.items():
        base = preset["base_weights"][criterion]
        final_score += (raw_score / base) * weights[criterion]
        evaluation["scores"][criterion]["total"] = round(raw_score, 2)

    final_score = round(final_score, 2)
    evaluation["final_score"] = final_score
    evaluation["score_label"] = score_label(final_score)
    evaluation["status"] = decide_status(evaluation, preset, final_score, scores)
    evaluation["updated_at"] = datetime.now(timezone.utc).isoformat()

    if args.dry_run:
        print(f"Final score: {final_score} ({evaluation['score_label']})")
        return 0

    write_json(evaluation_path, evaluation)
    print(f"Scored {evaluation_path}: {final_score} ({evaluation['score_label']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
