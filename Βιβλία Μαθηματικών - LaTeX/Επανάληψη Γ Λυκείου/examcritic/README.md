# ExamCritic MVP

Το `examcritic/` κρατά τις προδιαγραφές, τα machine-readable δεδομένα και τα templates για την πρώτη δοκιμή του αξιολογητή θεμάτων.

## Τρέχον MVP

Η πρώτη έκδοση αξιολογεί μόνο:

- Μάθημα: Μαθηματικά Γ΄ Λυκείου
- Εξέταση: Πανελλαδικές εξετάσεις
- Τύπος θέματος: Θέμα Γ
- Input: ένα `.tex` αρχείο τύπου `Θέματα/Γ/thema_G_XX.tex` ή copy-paste της εκφώνησης
- Scoring: χειροκίνητη αξιολόγηση με δομημένη φόρμα και βοηθητικά metadata

Η γενίκευση σε Θέματα Α, Β, Δ και σε άλλες τάξεις θα γίνει μετά το calibration αυτού του MVP.

## Φάκελοι

- `docs/`: αποφάσεις προϊόντος, rubric, scoring, workflow και acceptance tests.
- `data/`: JSON δεδομένα για ύλη, presets, taxonomy, rarity και corpus.
- `templates/`: πρότυπα εγγραφών αξιολόγησης, parsed metadata, report και προτάσεων βελτίωσης.
- `instructions/`: οδηγίες για τον αξιολογητή και για επιμέλεια θεμάτων.

## Πηγές repo

- `../implementation_plan.md`: αρχικό product plan.
- `../Θέματα/Γ/`: 100 διαθέσιμα Θέματα Γ.
- `../Λύσεις θεμάτων/Γ/`: 100 αντίστοιχες λύσεις.
- `../LLM Wiki Math Latex/wiki/ύλη/γ-λυκείου-μαθηματικά.md`: ύλη και έννοιες Γ΄ Λυκείου.

## Τρέχουσα ροή δοκιμής

Για χειροκίνητη αξιολόγηση με απλές ερωτήσεις:

```bash
python3 examcritic/scripts/evaluate_topic.py G-003
```

Για πρώτη αυτόματη rule-based αξιολόγηση:

```bash
python3 examcritic/scripts/auto_evaluate_topic.py G-003
```

Η αυτόματη αξιολόγηση παράγει report για έλεγχο καθηγητή. Δεν αντικαθιστά ακόμα τη μαθηματική κρίση.
