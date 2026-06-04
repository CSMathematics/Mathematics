---
title: Module Tables and Cases
tags: [latex, module, tables, cases]
updated: 2026-05-08
---

# Module Tables and Cases

## Στόχος

Ενιαία αντιμετώπιση για `cases`, πίνακες, πίνακες μεταβολών και πολυγραμμικούς υπολογισμούς.

## Κανόνες

- Piecewise ορισμοί με `cases`, όχι αυτοσχέδιες αγκύλες
- Πολυγραμμικοί υπολογισμοί με `align` ή `align*`
- Πίνακες μεταβολών με `tkz-tab` μόνο όταν προσφέρουν καθαρότερο αποτέλεσμα από λεκτική ανάλυση
- Απλοί πίνακες δεδομένων με καθαρό horizontal spacing και όχι υπερβολικά borders

## Ενδεικτικό Μοτίβο

```latex
f(x)=
\begin{cases}
  x^2, & x \ge 0,\\
  -x, & x < 0
\end{cases}
```

## Σχετικά

- [[latex/formatting-guide-lykeio]]
- [[latex/κλάδος/ανάλυση]]
