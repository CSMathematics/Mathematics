# LaTeX Ingestion Spec

## Στόχος MVP

Η ανάγνωση `.tex` στο MVP δεν προσπαθεί να καταλάβει όλα τα μαθηματικά. Στόχος είναι να βγάλει σταθερά metadata και να γεμίσει τη φόρμα αξιολόγησης.

## Supported input

Υποστηρίζονται αρχεία με δομή:

```latex
\begin{thema}{Γ}
...
\begin{erwthma}
\item ...
\item ...
\end{erwthma}
\end{thema}
```

Πηγή MVP:

```text
Θέματα/Γ/thema_G_XX.tex
```

Προαιρετική λύση:

```text
Λύσεις θεμάτων/Γ/solution_G_XX.tex
```

## Parsed fields

- `topic_id`: π.χ. `G-001`.
- `topic_letter`: `Γ`.
- `source_tex_path`.
- `solution_tex_path`, αν υπάρχει.
- `statement_raw`.
- `intro_text`: κείμενο πριν το `erwthma`.
- `subquestions`: λίστα με raw LaTeX ανά `\item`.
- `subquestion_count`.
- `latex_features`: πλήθος display math, inline math, tikz/pgfplots, tables.
- `parse_warnings`: λίστα μη μοιραίων προβλημάτων.

## Failure policy

- Αν δεν υπάρχει `\begin{thema}{Γ}`, το αρχείο απορρίπτεται.
- Αν δεν υπάρχει `\begin{erwthma}`, κρατιέται όλο το θέμα ως ένα block και μπαίνει warning.
- Αν δεν εντοπιστούν `\item`, ο χρήστης μπορεί να κάνει χειροκίνητο split.
- Αν λείπει λύση, η αξιολόγηση επιτρέπεται αλλά το Κ1 και το Κ7 σημειώνονται ως lower-confidence.

## Δεν κάνει στο MVP

- Δεν αποδεικνύει μαθηματική ορθότητα.
- Δεν υπολογίζει αυτόματα difficulty.
- Δεν αναγνωρίζει πλήρως nested environments.
- Δεν μετατρέπει LaTeX σε rendered HTML.

## Προτεινόμενη parser στρατηγική

- Plain text parsing με σαφή markers για την πρώτη έκδοση.
- Καμία μεταβολή στο αρχικό `.tex`.
- Τα parser outputs αποθηκεύονται σε `templates/topic-metadata.json` compatible shape.

