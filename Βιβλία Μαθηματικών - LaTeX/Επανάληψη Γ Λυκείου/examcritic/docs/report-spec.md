# Report Spec

## Στόχος report

Το report πρέπει να απαντά γρήγορα σε τρεις ερωτήσεις:

- Πόσο καλό είναι το θέμα συνολικά;
- Γιατί πήρε αυτό το score;
- Τι πρέπει να αλλάξει για να γίνει καλύτερο;

## Report sections

1. Summary

Περιλαμβάνει topic id, preset, final score, label, status και confidence.

2. Criterion breakdown

Περιλαμβάνει raw score, normalized contribution και σύντομη αιτιολόγηση για Κ1-Κ7.

3. Taxonomy snapshot

Περιλαμβάνει branches, question types, rare tags και ένδειξη μονοθεματικότητας.

4. Difficulty and time

Περιλαμβάνει raw difficulty factors, RD, target range, estimated time και time score.

5. Strengths

Σύντομη λίστα με τα 2-4 δυνατότερα σημεία.

6. Issues

Σύντομη λίστα με τα προβλήματα, ταξινομημένα σε critical, major, minor.

7. Improvement suggestions

Συγκεκριμένες προτάσεις αλλαγής εκφώνησης, δομής ή δυσκολίας.

## Comparison view

Η σύγκριση δύο θεμάτων δείχνει:

- final score και label.
- Κ1-Κ7 δίπλα δίπλα.
- taxonomy overlap.
- difficulty και time.
- ποιο θέμα είναι καλύτερο reference για διδασκαλία.

## Export contract

Το report μπορεί να εξαχθεί αρχικά ως JSON ή Markdown. PDF export μένει για μεταγενέστερη φάση.

