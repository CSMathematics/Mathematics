# ExamCritic Workspace

Εδώ μπαίνουν τα προσωρινά αρχεία δοκιμής του MVP.

## Φάκελοι

- `topics/`: parsed metadata από `.tex` θέματα.
- `evaluations/`: draft ή completed evaluation records.
- `reports/`: Markdown reports.

## Δοκιμή με τρία Θέματα Γ

```bash
python3 examcritic/scripts/parse_tex_topic.py Θέματα/Γ/thema_G_01.tex --overwrite
python3 examcritic/scripts/parse_tex_topic.py Θέματα/Γ/thema_G_02.tex --overwrite
python3 examcritic/scripts/parse_tex_topic.py Θέματα/Γ/thema_G_03.tex --overwrite

python3 examcritic/scripts/create_evaluation.py G-001 --overwrite
python3 examcritic/scripts/create_evaluation.py G-002 --overwrite
python3 examcritic/scripts/create_evaluation.py G-003 --overwrite
```

Μετά συμπληρώνεις τα JSON στο `evaluations/` και τρέχεις:

```bash
python3 examcritic/scripts/score_evaluation.py examcritic/workspace/evaluations/eval-G-001.json
python3 examcritic/scripts/report_evaluation.py examcritic/workspace/evaluations/eval-G-001.json --overwrite
```

## Πιο εύκολη αξιολόγηση

Αν δεν θέλεις να πειράζεις JSON, τρέξε:

```bash
python3 examcritic/scripts/evaluate_topic.py G-001
```

Θα σου κάνει απλές ερωτήσεις και στο τέλος θα ενημερώσει μόνο του το evaluation και το report.
