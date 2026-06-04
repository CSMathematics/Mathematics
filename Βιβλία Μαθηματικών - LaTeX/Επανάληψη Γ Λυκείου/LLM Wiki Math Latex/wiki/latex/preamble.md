---
title: Βασικό LaTeX Preamble
level: [bsc, msc, lyk]
tags: [latex]
updated: 2026-05-08
---

# Βασικό LaTeX Preamble

## Βασικό Preamble (όλα τα έγγραφα)

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[greek,english]{babel}
\usepackage{amsmath, amssymb, amsthm, mathtools}
\usepackage[a4paper, margin=2.5cm]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{enumitem}
\usepackage{xcolor}
```

⚠️ Για βιβλίο: `\documentclass[12pt,a4paper]{book}`

## Σχετικές σελίδες

- [[theorems]]
- [[exercises]]
- [[exam]]
