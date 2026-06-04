#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import (
    REPO_ROOT,
    WORKSPACE_DIR,
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
from score_evaluation import compute_scores, decide_status, normalized_weights


JsonPath = tuple[str, ...]


QUESTIONS: list[tuple[JsonPath, str, int, int]] = [
    (("scores", "K1", "indicators", "K1.1"), "Κ1.1 Είναι μαθηματικά σωστό το θέμα;", 0, 3),
    (("scores", "K1", "indicators", "K1.2"), "Κ1.2 Δίνονται όλα τα απαραίτητα δεδομένα;", 0, 3),
    (("scores", "K1", "indicators", "K1.3"), "Κ1.3 Είναι ακριβής η μαθηματική γλώσσα;", 0, 3),
    (("scores", "K1", "indicators", "K1.4"), "Κ1.4 Είναι συνεπής ο συμβολισμός;", 0, 3),
    (("scores", "K1", "indicators", "K1.5"), "Κ1.5 Είναι καθαρό το LaTeX/η τυπογραφία;", 0, 3),
    (("scores", "K2", "indicators", "K2.1"), "Κ2.1 Καταλαβαίνει ο μαθητής τι ζητείται με πρώτη ανάγνωση;", 0, 3),
    (("scores", "K2", "indicators", "K2.2"), "Κ2.2 Λείπουν περιττές πληροφορίες που μπερδεύουν;", 0, 2),
    (("scores", "K2", "indicators", "K2.3"), "Κ2.3 Είναι καθαρές οι εντολές των ερωτημάτων;", 0, 2),
    (("scores", "K2", "indicators", "K2.4"), "Κ2.4 Ταιριάζει η ορολογία με το σχολικό λεξιλόγιο;", 0, 3),
    (("scores", "K3", "indicators", "K3.1"), "Κ3.1 Τα ερωτήματα χτίζουν καλή αλυσίδα;", 0, 2),
    (("scores", "K3", "indicators", "K3.2"), "Κ3.2 Μπορεί ο μαθητής να συνεχίσει αν χάσει ένα προηγούμενο;", 0, 2),
    (("scores", "K3", "indicators", "K3.3"), "Κ3.3 Κλιμακώνεται φυσικά η δυσκολία;", 0, 2),
    (("scores", "K4", "indicators", "K4.1"), "Κ4.1 Πόσοι διαφορετικοί τύποι ερωτημάτων υπάρχουν; Βάλε 0-5.", 0, 5),
    (("scores", "K4", "indicators", "K4.2"), "Κ4.2 Πόσο καλά καλύπτει διαφορετικές ενότητες; Βάλε 0-8.", 0, 8),
    (("scores", "K4", "indicators", "K4.3"), "Κ4.3 Έχει σπάνια/λιγότερο συνηθισμένα ερωτήματα; Βάλε 0-4.", 0, 4),
    (("scores", "K4", "indicators", "K4.4"), "Κ4.4 Αποφεύγει τη μονοθεματικότητα; Βάλε 0-3.", 0, 3),
    (("difficulty", "technical_complexity"), "Δυσκολία υπολογισμών σε κλίμακα 0-10.", 0, 10),
    (("difficulty", "conceptual_depth"), "Βάθος θεωρητικής κατανόησης σε κλίμακα 0-10.", 0, 10),
    (("difficulty", "solution_steps"), "Πλήθος/μήκος βημάτων λύσης σε κλίμακα 0-10.", 0, 10),
    (("difficulty", "originality"), "Πρωτοτυπία σκέψης σε κλίμακα 0-10.", 0, 10),
    (("scores", "K6", "indicators", "K6.1"), "Κ6.1 Ελέγχει εννοιολογική κατανόηση;", 0, 4),
    (("scores", "K6", "indicators", "K6.2"), "Κ6.2 Έχει ανακαλυπτική πορεία;", 0, 4),
    (("scores", "K6", "indicators", "K6.3"), "Κ6.3 Μπορεί να γίνει παράδειγμα μεθόδου;", 0, 4),
    (("scores", "K6", "indicators", "K6.4"), "Κ6.4 Φανερώνει κοινές παρανοήσεις;", 0, 4),
    (("scores", "K6", "indicators", "K6.5"), "Κ6.5 Συνδέει θεωρία και εφαρμογή;", 0, 4),
    (("time", "estimated_minutes"), "Πόσα λεπτά πιστεύεις ότι χρειάζεται ένας καλά προετοιμασμένος μαθητής;", 1, 90),
]


def topic_id_to_tex_path(topic_id: str) -> Path:
    prefix, number = topic_id.split("-", 1)
    if prefix != "G":
        raise ValueError("Το interactive MVP υποστηρίζει προς το παρόν μόνο topic ids τύπου G-001.")
    return REPO_ROOT / "Θέματα" / "Γ" / f"thema_G_{int(number):02d}.tex"


def metadata_path(topic_id: str) -> Path:
    return WORKSPACE_DIR / "topics" / f"{topic_id}.metadata.json"


def evaluation_path(topic_id: str) -> Path:
    return WORKSPACE_DIR / "evaluations" / f"eval-{topic_id}.json"


def report_path(topic_id: str) -> Path:
    return WORKSPACE_DIR / "reports" / f"{topic_id}-report.md"


def get_nested(data: dict[str, Any], path: JsonPath) -> Any:
    current: Any = data
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def set_nested(data: dict[str, Any], path: JsonPath, value: Any) -> None:
    parts = path
    current = data
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value


def ask_number(path: str, label: str, minimum: int, maximum: int, current: Any) -> int | float:
    current_text = f" [τρέχον: {current}]" if current is not None else ""
    while True:
        raw = input(f"{label} ({minimum}-{maximum}){current_text}: ").strip()
        if raw == "" and current is not None:
            return current
        try:
            value = float(raw.replace(",", "."))
        except ValueError:
            print("Βάλε έναν αριθμό.")
            continue

        if value < minimum or value > maximum:
            print(f"Ο αριθμός πρέπει να είναι από {minimum} έως {maximum}.")
            continue

        if value.is_integer():
            return int(value)
        return value


def ask_list(title: str, current: list[str]) -> list[str]:
    current_text = "; ".join(current)
    prompt = f"{title}"
    if current_text:
        prompt += f" [τρέχον: {current_text}]"
    prompt += " (προαιρετικά, χώρισε με ;): "
    raw = input(prompt).strip()
    if raw == "":
        return current
    return [item.strip() for item in raw.split(";") if item.strip()]


def ensure_metadata(topic_id: str) -> dict[str, Any]:
    path = metadata_path(topic_id)
    if path.exists():
        return load_json(path)

    topic_path = topic_id_to_tex_path(topic_id)
    if not topic_path.exists():
        raise FileNotFoundError(topic_path)

    metadata = build_metadata(topic_path, None, topic_id)
    write_json(path, metadata)
    return metadata


def ensure_evaluation(topic_id: str, metadata: dict[str, Any], evaluator: str) -> dict[str, Any]:
    path = evaluation_path(topic_id)
    if path.exists():
        return load_json(path)
    return build_evaluation(metadata, evaluator)


def reset_auto_scores(evaluation: dict[str, Any]) -> None:
    for criterion in ["K1", "K2", "K3", "K4", "K5", "K6", "K7"]:
        evaluation["scores"][criterion]["total"] = None
    evaluation["final_score"] = None
    evaluation["score_label"] = ""


def score_in_memory(evaluation: dict[str, Any]) -> tuple[float, list[str]]:
    preset = load_active_preset(evaluation["preset_id"])
    scores, missing = compute_scores(evaluation, preset)
    if missing:
        return 0.0, sorted(set(missing))

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
    return final_score, []


def print_topic(metadata: dict[str, Any]) -> None:
    print()
    print(f"Θέμα: {metadata['topic_id']} ({metadata.get('source_tex_path', '')})")
    print()
    if metadata.get("intro_text"):
        print(metadata["intro_text"])
        print()
    for subquestion in metadata.get("subquestions", []):
        print(f"{subquestion['id']}. {subquestion['text_raw']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Interactive terminal evaluation for a Θέμα Γ.")
    parser.add_argument("topic_id", help="Topic id, e.g. G-001")
    parser.add_argument("--evaluator", default="", help="Evaluator name or initials")
    parser.add_argument("--no-topic", action="store_true", help="Do not print topic text before questions")
    args = parser.parse_args()

    topic_id = args.topic_id.upper()
    metadata = ensure_metadata(topic_id)
    evaluation = ensure_evaluation(topic_id, metadata, args.evaluator)
    if args.evaluator:
        evaluation["evaluator"]["name"] = args.evaluator

    print("ExamCritic απλή αξιολόγηση")
    print("Πάτα Enter για να κρατήσεις υπάρχουσα τιμή.")

    if not args.no_topic:
        print_topic(metadata)

    reset_auto_scores(evaluation)
    for path, label, minimum, maximum in QUESTIONS:
        value = ask_number(path, label, minimum, maximum, get_nested(evaluation, path))
        set_nested(evaluation, path, value)

    notes = evaluation.setdefault("notes", {})
    notes["strengths"] = ask_list("Δυνατά σημεία", notes.get("strengths", []))
    notes["issues"] = ask_list("Προβλήματα", notes.get("issues", []))
    notes["improvement_suggestions"] = ask_list(
        "Προτάσεις βελτίωσης", notes.get("improvement_suggestions", [])
    )

    final_score, missing = score_in_memory(evaluation)
    if missing:
        print("Λείπουν ακόμα πεδία:")
        for field in missing:
            print(f"- {field}")
        return 2

    eval_path = evaluation_path(topic_id)
    rep_path = report_path(topic_id)
    write_json(eval_path, evaluation)
    write_text(rep_path, build_report(evaluation))

    print()
    print(f"Αποθηκεύτηκε: {repo_relative(eval_path)}")
    print(f"Report: {repo_relative(rep_path)}")
    print(f"Τελικό score: {final_score} ({evaluation['score_label']})")
    print(f"Status: {evaluation['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
