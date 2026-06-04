# ExamCritic Scripts

Το MVP τρέχει με ένα μικρό CLI loop:

```bash
python3 examcritic/scripts/parse_tex_topic.py Θέματα/Γ/thema_G_01.tex --overwrite
python3 examcritic/scripts/create_evaluation.py G-001 --evaluator "Σ.Μ." --overwrite
python3 examcritic/scripts/score_evaluation.py examcritic/workspace/evaluations/eval-G-001.json
python3 examcritic/scripts/report_evaluation.py examcritic/workspace/evaluations/eval-G-001.json --overwrite
```

Το `score_evaluation.py` χρειάζεται συμπληρωμένα scores. Αν λείπουν πεδία, τυπώνει λίστα με όσα πρέπει να συμπληρωθούν.

Το Κ5 υπολογίζεται αυτόματα από τα πεδία `difficulty.*`.
Το Κ7 υπολογίζεται αυτόματα από το `time.estimated_minutes`.

## Πιο απλή χρήση

Για να μη γράφεις JSON με το χέρι, χρησιμοποίησε την απλή φόρμα:

```bash
python3 examcritic/scripts/evaluate_topic.py G-002
```

Το script ρωτάει τους βαθμούς έναν έναν, αποθηκεύει το evaluation και ενημερώνει το report.

## Πρώτη αυτόματη αξιολόγηση

Για rule-based αυτόματη πρώτη εκτίμηση:

```bash
python3 examcritic/scripts/auto_evaluate_topic.py G-003
```

Το αποτέλεσμα χρειάζεται έλεγχο καθηγητή. Είναι αρχικό report, όχι τελική μαθηματική κρίση.
