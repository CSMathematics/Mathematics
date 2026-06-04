#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import (
    EXAMCRITIC_DIR,
    REPO_ROOT,
    WORKSPACE_DIR,
    clamp,
    load_active_preset,
    load_json,
    repo_relative,
    score_label,
    write_json,
    write_text,
)
from create_evaluation import build_evaluation
from parse_tex_topic import build_metadata
from report_evaluation import build_report
from score_evaluation import compute_scores, normalized_weights


RULESET_VERSION = "rule_based_v0.1"


def topic_id_to_tex_path(topic_id: str) -> Path:
    prefix, number = topic_id.split("-", 1)
    if prefix != "G":
        raise ValueError("Το auto MVP υποστηρίζει προς το παρόν μόνο topic ids τύπου G-001.")
    return REPO_ROOT / "Θέματα" / "Γ" / f"thema_G_{int(number):02d}.tex"


def metadata_path(topic_id: str) -> Path:
    return WORKSPACE_DIR / "topics" / f"{topic_id}.metadata.json"


def evaluation_path(topic_id: str) -> Path:
    return WORKSPACE_DIR / "evaluations" / f"eval-{topic_id}.json"


def report_path(topic_id: str) -> Path:
    return WORKSPACE_DIR / "reports" / f"{topic_id}-report.md"


def load_rarity() -> dict[str, str]:
    taxonomy = load_json(EXAMCRITIC_DIR / "data" / "taxonomy" / "question-types.json")
    return {
        item["id"]: item.get("default_rarity", "common")
        for item in taxonomy.get("question_types", [])
    }


def normalize(text: str) -> str:
    return text.lower().replace("ά", "α").replace("έ", "ε").replace("ή", "η").replace(
        "ί", "ι"
    ).replace("ό", "ο").replace("ύ", "υ").replace("ώ", "ω")


def has_any(text: str, patterns: list[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def detect_question_types(text: str) -> set[str]:
    ntext = normalize(text)
    types: set[str] = set()

    if has_any(ntext, ["τυπος της", "να βρειτε τον τυπο", "να δειξετε οτι ο τυπος"]):
        types.add("recover_function_from_condition")
    if has_any(ntext, ["πεδιο ορισμου", "συνολο τιμων"]):
        types.add("domain_or_range")
    if has_any(ntext, ["οριο", r"\lim"]):
        types.add("limit_evaluation")
    if has_any(ntext, ["συνεχ"]):
        types.add("continuity_argument")
    if has_any(ntext, ["παραγωγ", "f'", r"\prime"]):
        types.add("derivative_computation")
    if has_any(ntext, ["μονοτον", "ακροτατ", "μεγιστ", "ελαχιστ"]):
        types.add("monotonicity_extrema")
    if has_any(ntext, ["bolzano"]):
        types.add("existence_bolzano")
    if "υπαρχει" in ntext and has_any(ntext, ["τουλαχιστον", "ριζα", "x_0", "ξ"]):
        types.add("existence_bolzano")
    if has_any(ntext, ["rolle", "μεσης τιμης", "θμτ"]):
        types.add("existence_mvt_rolle")
    if has_any(ntext, ["\\le", "\\ge", "≤", "≥", " ανισοτ", "ισχυει"]):
        types.add("inequality_proof")
    if has_any(ntext, ["εφαπτομ"]):
        types.add("tangent_line")
    if has_any(ntext, ["ρυθμο", "μεταβαλλεται", "κινειται"]):
        types.add("rate_of_change")
    if has_any(ntext, [r"\int", "ολοκληρ"]):
        types.add("integral_calculation")
    if has_any(ntext, ["εμβαδ"]):
        types.add("area_between_curves")
    if has_any(ntext, ["κυρτοτ", "καμπης"]):
        types.add("convexity_inflection")
    if has_any(ntext, ["ασυμπτω"]):
        types.add("asymptote_detection")
    if has_any(ntext, ["παραμετρ", " α ", "β >"]):
        types.add("parameter_condition")
    if has_any(ntext, ["γραφικη παρασταση", "c_f"]):
        types.add("graph_interpretation")
    if has_any(ntext, ["αντιστροφη", "συνθεση", "f\\circ"]):
        types.add("composition_or_inverse")

    return types


def branches_for_types(question_types: set[str]) -> set[str]:
    branches: set[str] = set()
    mapping = {
        "domain_or_range": {"limits_continuity"},
        "limit_evaluation": {"limits_continuity"},
        "continuity_argument": {"limits_continuity"},
        "derivative_computation": {"derivatives"},
        "monotonicity_extrema": {"derivatives", "monotonicity_extrema"},
        "existence_bolzano": {"limits_continuity", "mean_value_theorems"},
        "existence_mvt_rolle": {"derivatives", "mean_value_theorems"},
        "inequality_proof": {"inequalities", "derivatives"},
        "tangent_line": {"derivatives"},
        "rate_of_change": {"rates_of_change", "derivatives"},
        "integral_calculation": {"integrals"},
        "area_between_curves": {"integrals", "area_applications"},
        "convexity_inflection": {"derivatives", "convexity_inflection"},
        "asymptote_detection": {"limits_continuity", "asymptotes_lhospital"},
        "parameter_condition": {"parameter_analysis"},
        "graph_interpretation": {"graph_study"},
        "composition_or_inverse": {"limits_continuity"},
        "recover_function_from_condition": {"derivatives"},
    }
    for question_type in question_types:
        branches.update(mapping.get(question_type, set()))
    return branches


def tag_metadata(metadata: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    rarity = load_rarity()
    all_types: set[str] = set()
    all_branches: set[str] = set()

    for subquestion in metadata.get("subquestions", []):
        detected_types = detect_question_types(subquestion.get("text_raw", ""))
        detected_branches = branches_for_types(detected_types)
        subquestion["question_types"] = sorted(detected_types)
        subquestion["branches"] = sorted(detected_branches)
        all_types.update(detected_types)
        all_branches.update(detected_branches)

    rare_types = sorted(
        question_type for question_type in all_types if rarity.get(question_type) == "rare"
    )
    return sorted(all_branches), sorted(all_types), rare_types


def estimate_monothematicity(branches: list[str], question_types: list[str]) -> int:
    if len(branches) >= 4 and len(question_types) >= 4:
        return 3
    if len(branches) >= 3 and len(question_types) >= 3:
        return 2
    if len(branches) >= 2:
        return 1
    return 0


def estimate_difficulty(metadata: dict[str, Any], question_types: list[str], rare_types: list[str]) -> dict:
    subquestion_count = metadata.get("subquestion_count") or 0
    features = metadata.get("latex_features", {})
    display_math = features.get("display_math_count") or 0
    inline_math = features.get("inline_math_count") or 0

    technical = 3.5 + 0.45 * subquestion_count + 0.25 * display_math + 0.05 * inline_math
    if {"integral_calculation", "area_between_curves", "tangent_line"} & set(question_types):
        technical += 1

    conceptual = 4 + 0.6 * len(set(question_types))
    if {"existence_bolzano", "existence_mvt_rolle", "inequality_proof"} & set(question_types):
        conceptual += 1

    steps = 2.5 + 1.1 * subquestion_count + 0.3 * len(set(question_types))
    originality = 3.5 + 0.6 * len(rare_types)
    if {"rate_of_change", "parameter_condition", "graph_interpretation"} & set(question_types):
        originality += 1
    if {"inequality_proof", "existence_bolzano", "existence_mvt_rolle"} & set(question_types):
        originality += 0.5

    return {
        "technical_complexity": round(clamp(technical, 0, 10), 1),
        "conceptual_depth": round(clamp(conceptual, 0, 10), 1),
        "solution_steps": round(clamp(steps, 0, 10), 1),
        "originality": round(clamp(originality, 0, 10), 1),
        "raw_difficulty": None,
    }


def estimate_time_minutes(metadata: dict[str, Any], question_types: list[str], rare_types: list[str]) -> int:
    subquestion_count = metadata.get("subquestion_count") or 0
    minutes = 9 + 3.2 * subquestion_count + 1.3 * len(set(question_types)) + 1.5 * len(rare_types)
    if {"integral_calculation", "area_between_curves"} & set(question_types):
        minutes += 2
    return round(clamp(minutes, 12, 45))


def auto_scores(metadata: dict[str, Any], branches: list[str], question_types: list[str], rare_types: list[str]) -> dict:
    warnings = metadata.get("parse_warnings", [])
    solution_exists = bool(metadata.get("solution_tex_path"))
    subquestion_count = metadata.get("subquestion_count") or 0
    features = metadata.get("latex_features", {})

    k1_1 = 2 if solution_exists else 1
    k1_2 = 3 if 3 <= subquestion_count <= 5 else 2
    k1_3 = 2
    k1_4 = 2
    k1_5 = 3 if not warnings else 2

    k2_1 = 2
    k2_2 = 2
    k2_3 = 2 if subquestion_count >= 3 else 1
    k2_4 = 3

    k3_1 = 2 if subquestion_count >= 4 else 1
    k3_2 = 1
    k3_3 = 2 if 3 <= subquestion_count <= 5 else 1

    k4_1 = min(len(question_types), 5)
    k4_2 = min(len(branches) * 2, 8)
    k4_3 = min(len(rare_types), 4)
    k4_4 = estimate_monothematicity(branches, question_types)

    concept_types = {"existence_bolzano", "existence_mvt_rolle", "inequality_proof", "rate_of_change"}
    application_types = {"rate_of_change", "tangent_line", "area_between_curves", "graph_interpretation"}
    k6_1 = 3 if concept_types & set(question_types) else 2
    k6_2 = 3 if k3_1 == 2 and len(question_types) >= 4 else 2
    k6_3 = 3 if len(question_types) >= 4 else 2
    k6_4 = 2 if concept_types & set(question_types) else 1
    k6_5 = 3 if application_types & set(question_types) else 2

    if features.get("tikz_or_pgfplots"):
        k1_5 = min(k1_5, 2)

    return {
        "K1": {"K1.1": k1_1, "K1.2": k1_2, "K1.3": k1_3, "K1.4": k1_4, "K1.5": k1_5},
        "K2": {"K2.1": k2_1, "K2.2": k2_2, "K2.3": k2_3, "K2.4": k2_4},
        "K3": {"K3.1": k3_1, "K3.2": k3_2, "K3.3": k3_3},
        "K4": {"K4.1": k4_1, "K4.2": k4_2, "K4.3": k4_3, "K4.4": k4_4},
        "K6": {"K6.1": k6_1, "K6.2": k6_2, "K6.3": k6_3, "K6.4": k6_4, "K6.5": k6_5},
    }


def apply_auto_scores(evaluation: dict[str, Any], scores: dict[str, dict[str, int]]) -> None:
    for criterion, indicators in scores.items():
        evaluation["scores"][criterion]["indicators"] = indicators
        evaluation["scores"][criterion]["total"] = None
    for criterion in ["K5", "K7"]:
        evaluation["scores"][criterion]["total"] = None


def score_evaluation(evaluation: dict[str, Any]) -> float:
    preset = load_active_preset(evaluation["preset_id"])
    scores, missing = compute_scores(evaluation, preset)
    if missing:
        raise ValueError("Auto evaluation left missing fields: " + ", ".join(sorted(set(missing))))

    weights = normalized_weights(preset)
    final_score = 0.0
    for criterion, raw_score in scores.items():
        base = preset["base_weights"][criterion]
        final_score += (raw_score / base) * weights[criterion]
        evaluation["scores"][criterion]["total"] = round(raw_score, 2)

    final_score = round(final_score, 2)
    evaluation["final_score"] = final_score
    evaluation["score_label"] = score_label(final_score)
    evaluation["status"] = "review"
    evaluation["updated_at"] = datetime.now(timezone.utc).isoformat()
    return final_score


def topic_id_from_arg(value: str) -> str:
    if re.fullmatch(r"[A-Za-z]-\d+", value):
        prefix, number = value.upper().split("-", 1)
        return f"{prefix}-{int(number):03d}"
    path = Path(value)
    match = re.search(r"thema_G_(\d+)\.tex$", path.name)
    if match:
        return f"G-{int(match.group(1)):03d}"
    raise ValueError("Use a topic id like G-003 or a thema_G_XX.tex path.")


def input_topic_path(value: str, topic_id: str) -> Path:
    candidate = Path(value)
    if candidate.suffix == ".tex":
        return candidate if candidate.is_absolute() else REPO_ROOT / candidate
    return topic_id_to_tex_path(topic_id)


def existing_manual_evaluation(path: Path) -> bool:
    if not path.exists():
        return False
    data = load_json(path)
    if data.get("automation", {}).get("mode") == RULESET_VERSION:
        return False
    if data.get("final_score") is not None:
        return True
    for criterion in data.get("scores", {}).values():
        if criterion.get("total") is not None:
            return True
        indicators = criterion.get("indicators", {})
        if any(value is not None for value in indicators.values()):
            return True
    difficulty = data.get("difficulty", {})
    if any(value is not None for value in difficulty.values()):
        return True
    return data.get("time", {}).get("estimated_minutes") is not None


def build_notes(evaluation: dict[str, Any], branches: list[str], question_types: list[str]) -> None:
    notes = evaluation.setdefault("notes", {})
    notes["strengths"] = [
        f"Αυτόματη αναγνώριση {len(question_types)} τύπων ερωτημάτων.",
        f"Αυτόματη αναγνώριση {len(branches)} ενοτήτων/κλάδων ύλης.",
    ]
    notes["issues"] = [
        "Η μαθηματική ορθότητα δεν αποδεικνύεται από τους κανόνες και χρειάζεται έλεγχο καθηγητή.",
        "Η διδακτική αξία είναι rule-based εκτίμηση και χρειάζεται επιβεβαίωση.",
    ]
    notes["improvement_suggestions"] = [
        "Έλεγξε αν τα αυτόματα taxonomy tags ταιριάζουν πραγματικά με τη λύση.",
        "Διόρθωσε χειροκίνητα τους δείκτες Κ1 και Κ6 αν η αυτόματη κρίση είναι άδικη.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Rule-based automatic ExamCritic evaluation.")
    parser.add_argument("topic", help="Topic id like G-003 or path to thema_G_XX.tex")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing evaluation")
    parser.add_argument("--evaluator", default="auto", help="Evaluator label")
    args = parser.parse_args()

    topic_id = topic_id_from_arg(args.topic)
    topic_path = input_topic_path(args.topic, topic_id)
    if not topic_path.exists():
        raise FileNotFoundError(topic_path)

    eval_path = evaluation_path(topic_id)
    if existing_manual_evaluation(eval_path) and not args.overwrite:
        raise FileExistsError(
            f"{repo_relative(eval_path)} already has a manual/completed evaluation. Use --overwrite."
        )

    metadata = build_metadata(topic_path, None, topic_id)
    branches, question_types, rare_types = tag_metadata(metadata)
    write_json(metadata_path(topic_id), metadata)

    evaluation = build_evaluation(metadata, args.evaluator)
    evaluation["taxonomy"] = {
        "branches": branches,
        "question_types": question_types,
        "rare_question_types": rare_types,
        "monothematicity_score": estimate_monothematicity(branches, question_types),
    }
    evaluation["difficulty"] = estimate_difficulty(metadata, question_types, rare_types)
    evaluation["time"] = {"estimated_minutes": estimate_time_minutes(metadata, question_types, rare_types)}
    apply_auto_scores(evaluation, auto_scores(metadata, branches, question_types, rare_types))
    build_notes(evaluation, branches, question_types)
    evaluation["automation"] = {
        "mode": RULESET_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "requires_teacher_review": True,
        "review_fields": ["K1", "K2", "K6", "taxonomy", "difficulty", "time"],
        "confidence": {
            "parse": "high" if not metadata.get("parse_warnings") else "medium",
            "taxonomy": "medium",
            "mathematical_soundness": "low",
            "pedagogical_value": "low",
            "difficulty": "medium",
            "time": "medium",
        },
    }

    final_score = score_evaluation(evaluation)
    write_json(eval_path, evaluation)
    write_text(report_path(topic_id), build_report(evaluation))

    print(f"Auto evaluation: {repo_relative(eval_path)}")
    print(f"Report: {repo_relative(report_path(topic_id))}")
    print(f"Score: {final_score} ({evaluation['score_label']})")
    print("Status: review (χρειάζεται έλεγχο καθηγητή)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
