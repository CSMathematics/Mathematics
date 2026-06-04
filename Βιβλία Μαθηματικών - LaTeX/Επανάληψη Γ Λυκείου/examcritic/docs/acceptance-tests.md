# Acceptance Tests

Οι παρακάτω δοκιμές ορίζουν τι σημαίνει να δουλεύει σωστά το MVP.

## Functional tests

1. Φόρτωση `Θέματα/Γ/thema_G_01.tex` παράγει `topic_letter = Γ` και 4 υποερωτήματα.
2. Θέμα χωρίς `\begin{erwthma}` δεν απορρίπτεται, αλλά παίρνει parse warning.
3. Θέμα χωρίς `\begin{thema}{Γ}` απορρίπτεται ως unsupported.
4. Evaluation record με όλα τα indicator scores παράγει final score 0-100.
5. Αν Κ1.1 είναι 0, το status δεν μπορεί να γίνει `approved`.
6. Αν RD είναι 6, το Κ5 είναι 15.
7. Αν RD είναι 4, το Κ5 είναι 12.
8. Αν estimated time είναι 25, το Κ7 είναι 10.
9. Αν estimated time είναι 35, το Κ7 είναι περίπου 4.4.
10. Αν Κ4 έχει 5 question types, 4 branches, 2 rare tags και variety 3, τότε Κ4 είναι 18.

## Calibration tests

1. Πέντε γνωστά Θέματα Γ αξιολογούνται από δύο καθηγητές.
2. Η μέση απόκλιση final score πρέπει να είναι μέχρι 8 μονάδες.
3. Η απόκλιση Κ5 πρέπει να είναι μέχρι 3 μονάδες μετά από συζήτηση calibration.
4. Τα taxonomy tags πρέπει να συμφωνούν τουλάχιστον κατά 70%.

## Data integrity tests

1. Κάθε evaluation έχει `preset_id`.
2. Κάθε evaluation έχει `topic_id`.
3. Κάθε score είναι εντός των ορίων του rubric.
4. Κάθε question type υπάρχει στο `data/taxonomy/question-types.json`.
5. Κάθε branch υπάρχει στο `data/taxonomy/chapters-and-branches.json`.

