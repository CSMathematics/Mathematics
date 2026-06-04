---
title: Module Common Macros
tags: [latex, module, macros]
updated: 2026-05-08
---

# Module Common Macros

## Στόχος

Κοινές μακροεντολές για να μένει η σημειογραφία σταθερή και να αποφεύγεται ο κατακερματισμός μεταξύ αρχείων.

## Προτεινόμενες Μακροεντολές

```latex
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\abs}[1]{\left|#1\right|}
\newcommand{\norm}[1]{\left\lVert#1\right\rVert}
\newcommand{\set}[1]{\left\{#1\right\}}
\newcommand{\d}{\mathop{}\!\mathrm{d}}

% Βοηθητικές Εντολές (από school_book_template)
\newcommand{\lysh}{\textcolor{secondcolor}{\noindent\faCheck\ \textbf{ΛΥΣΗ}}\\}
\newcommand{\bhmata}{\textcolor{maincolor!80!black}{{\large \textbf{Βήματα}\\\vspace{-7mm}}}}
\newcommand{\tropoi}{\textcolor{maincolor!80!black}{{\large \textbf{Τρόποι}\\\vspace{-7mm}}}}
\newcommand{\apanthsh}{{\textbf{ΑΠΑΝΤΗΣΗ}}\\}
\newcommand{\tss}[1]{\textsuperscript{#1}}
\newcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=2pt] (char) {#1};}}
\newcommand{\dlh}[1]{\xlongequal[\text{\eng{DLH}}]{#1}}
\newcommand{\true}{\textcolor{check}{\faCheck}{\ \ Αληθές}}
\newcommand{\false}{\textcolor{error}{\faTimes}{\ \ Ψευδές}}
\newcommand{\theor}[1]{\tikz[baseline=(char.base)]{\node[shape=circle,fill=maincolor,inner sep=2pt] (char) {\textcolor{white}{1}};}\ { Θεώρημα: #1\\}}
```

## Κανόνες

- Τα macros να δηλώνονται μία φορά στο preamble ή σε shared include
- Να αποφεύγονται macros που κρύβουν βασική μαθηματική δομή
- Αν ένα έγγραφο χρησιμοποιεί `\vect`, να μη συνυπάρχει με δεύτερη ανταγωνιστική macro για διανύσματα
