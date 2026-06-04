---
title: Οδηγός Μορφοποίησης Λύσεων Γ Λυκείου
branches: [lykeio]
level: [lyk]
tags: [latex, exercises, formatting]
sources: [FORMATTING_GUIDE.md]
updated: 2026-05-08
---

# Οδηγός Μορφοποίησης Λύσεων Γ Λυκείου

**Σύνοψη**: Προδιαγραφές σύνταξης και στυλ για αρχεία λύσεων LaTeX στα μαθηματικά Γ΄ Λυκείου (Επανάληψη Γ Λυκείου). Ορίζει τα περιβάλλοντα, τη μαθηματική σύνταξη, τους πίνακες μεταβολών, τις γραφικές παραστάσεις και τους περιορισμούς ύλης.

**Πηγές**: raw/FORMATTING_GUIDE.md

---

## 1. Δομή Αρχείου & Περιβάλλοντα

Κάθε λύση κλείνεται στο περιβάλλον `thema` και τα ερωτήματα στο `erwthma`:

```latex
%=========== ΛΥΣΗ - 1ο ΘΕΜΑ Β ===========
\begin{thema}{Β}
\begin{erwthma}
\item Λύση πρώτου ερωτήματος...
\item Λύση δεύτερου ερωτήματος...
\end{erwthma}
\end{thema}
```

**Κανόνας αρχείου**: Κάθε αρχείο περιέχει **μόνο κώδικα LaTeX** — χωρίς οδηγίες, χωρίς σχόλια μέσα στη λύση, χωρίς αντιγραφή εκφώνησης.

---

## 2. Μαθηματική Σύνταξη

| Τύπος | Σύνταξη |
|-------|---------|
| Inline math | `$ ... $` |
| Display math | `\[ ... \]` |
| Πολυγραμμικοί υπολογισμοί | `\begin{align*} ... \end{align*}` (ευθυγράμμιση στο `=`) |
| Ανάλυση ριζών/προσήμων | `\begin{itemize}` με `$f'(x)=0\Leftrightarrow\dots$` |

**Ορολογία & Έμφαση:**
- Θεωρήματα / τεχνικοί όροι: `\eng{DLH}`, `\eng{Fermat}` — **όχι** αγγλικά χωρίς `\eng`
- Κρίσιμοι όροι: `\textbf{γνησίως αύξουσα}`

---

## 3. Πίνακες Μεταβολών (tkz-tab)

Όλοι οι πίνακες εντός `\begin{center}...\end{center}` με:

```latex
\begin{center}
\begin{tikzpicture}
  \tkzTabInit[colorC=red7, colorL=red9, colorV=red7]
    {$x$ / 1, $f'(x)$ / 1, $f(x)$ / 2}
    {$a$, $b$}
  \tkzTabLine{, +, z, -,}
  \tkzTabVar{-/, +/$M$, -/}
\end{tikzpicture}
\end{center}
```

**Σύμβολα μονοτονίας**: `\searrow`, `\nearrow`, `z` (ρίζα), `t` (τοπικό ακρότατο)

**Σύμβολα κυρτότητας**: `\curvearrowright` (κοίλη), `\rotatebox[origin=c]{180}{$\curvearrowleft$}` (κυρτή)

---

## 4. Γραφικές Παραστάσεις (pgfplots)

Αυστηρά με `pgfplots`. Πρότυπο:

```latex
\begin{tikzpicture}
\begin{axis}[
    width=6.5cm, height=5.5cm,
    xmin=..., xmax=..., ymin=..., ymax=...,
    xtick={...}, ytick={...},
    xlabel={\footnotesize $ x $},
    ylabel={\footnotesize $ y $},
    grid=both,
    grid style={line width=.1pt, draw=gray!10},
    major grid style={line width=.2pt, draw=gray!50},
    minor tick num=4
]
\begin{scope}
    \clip (axis cs:xmin,ymin) rectangle (axis cs:xmax,ymax);
    \addplot[grafikh parastash, domain=..., secondcolor]{...};
\end{scope}
\node at (axis cs:0,0) {\footnotesize$O$};
\end{axis}
\end{tikzpicture}
```

---

## 5. Ειδικές Εντολές

| Εντολή | Χρήση |
|--------|-------|
| `\hm`, `\syn`, `\ef`, `\syf` | Τριγωνομετρικές συναρτήσεις στα ελληνικά — **ποτέ** αγγλικοί όροι |
| `\d x` | Διαφορικό σε ολοκληρώματα (π.χ. `\int_a^b f(x)\,\d x`) |
| `\lim_{x \to a}` | Όρια |
| `\xlongequal` | Βήματα L'Hôpital |
| `\eng{...}` | Αγγλικά ονόματα θεωρημάτων |

---

## 6. Περιορισμοί Ύλης (Γ Λυκείου)

Οι παρακάτω έννοιες είναι **εκτός ύλης** και δεν χρησιμοποιούνται:

- **Αόριστα ολοκληρώματα** — χρήση μόνο ορισμένων
- **Κριτήριο 2ης παραγώγου** για τοπικά ακρότατα
- **Διαφορικές εξισώσεις**
- **Θεώρημα Μέσης Τιμής Ολοκληρωτικού Λογισμού** (ΘΜΤ) ως τεκμηρίωση
- **Ολοκληρώματα με μεταβλητά άκρα** — διαφοροποίηση $\int_{a}^{g(x)} f(t)\,dt$

---

## Σχετικές σελίδες

- [[exercises]]
- [[exam]]
- [[lykeio]]
- [[conventions/analysis]]
