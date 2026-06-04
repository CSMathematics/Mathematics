---
title: Module PGFPlots Functions
tags: [latex, module, pgfplots, graphs]
updated: 2026-05-08
---

# Module PGFPlots Functions

## Στόχος

Ενιαίες προδιαγραφές για γραφικές παραστάσεις συναρτήσεων, καμπύλες και άξονες ώστε να υπάρχει κοινή οπτική γλώσσα.

## Πακέτα

```latex
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
```

## Βασικό Axis Style

```latex
\begin{axis}[
  axis lines=middle,
  width=7cm,
  height=5.5cm,
  grid=both,
  grid style={line width=.1pt, draw=gray!15},
  major grid style={line width=.2pt, draw=gray!40},
  xmin=-4, xmax=4,
  ymin=-4, ymax=4,
  xlabel={$x$},
  ylabel={$y$}
]
\addplot[domain=-3:3, samples=150, thick] {x^2-1};
\end{axis}
```

## Κανόνες

- Για λείες καμπύλες να ορίζεται επαρκές `samples`
- Για ασύμπτωτες, κομμάτια ή περιορισμένα domains να χρησιμοποιούνται ξεχωριστά `\addplot`
- Τα ειδικά σημεία να σημειώνονται καθαρά με `\addplot coordinates` ή `\node`
- Το εύρος αξόνων να επιλέγεται με μαθηματικό νόημα και όχι αυθαίρετα

## Καλύπτει

- Πολυωνυμικές, ρητές, εκθετικές, λογαριθμικές, τριγωνομετρικές συναρτήσεις
- Piecewise γραφικές παραστάσεις
- Παραβολές, κύκλους και βασικές κωνικές όταν η αναπαράσταση είναι πιο λειτουργική σε άξονες
