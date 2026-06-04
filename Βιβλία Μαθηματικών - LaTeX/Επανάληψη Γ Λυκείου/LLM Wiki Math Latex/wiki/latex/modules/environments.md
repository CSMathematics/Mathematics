---
title: Περιβάλλοντα και Κουτιά
level: [gym, lyk, bsc, msc]
tags: [latex, modules, environments, tcolorbox]
updated: 2026-05-08
---

# Περιβάλλοντα (Environments & tcolorbox)

Για τα βοηθήματα (Λύκειο/Γυμνάσιο) χρησιμοποιείται το πακέτο `tcolorbox` για όμορφα, χρωματιστά περιβάλλοντα. Για πανεπιστημιακές σημειώσεις (bsc/msc) συχνά χρησιμοποιούνται τα απλά `\newtheorem` του `amsthm`.

## 1. Κουτιά με tcolorbox (Βοηθήματα Γυμνασίου/Λυκείου)

Απαιτείται το πακέτο `\usepackage[most]{tcolorbox}`.
Τα βασικά περιβάλλοντα είναι:

```latex
\begin{parat}{\linewidth}
Κείμενο παρατήρησης...
\end{parat}

\begin{thema}{1}
Περιεχόμενο θέματος 1...
\end{thema}

\begin{askhsh}{Τίτλος Άσκησης}
Εκφώνηση άσκησης...
\end{askhsh}

\begin{problhma}{Τίτλος Προβλήματος}
Εκφώνηση προβλήματος...
\end{problhma}

\begin{prosoxi}{\linewidth}
Κείμενο προσοχής...
\end{prosoxi}

\begin{Thewrhmabox}{Τίτλος Θεωρήματος}
Διατύπωση θεωρήματος...
\end{Thewrhmabox}

\begin{Orismosbox}{Όνομα Ορισμού}
Κείμενο ορισμού...
\end{Orismosbox}

\begin{Αntiparadeigmabox}{Τίτλος}
Κείμενο αντιπαραδείγματος...
\end{Αntiparadeigmabox}
```

## 2. Εντολές Επικεφαλίδων (Inline Εντολές)

Μπορείτε να χρησιμοποιήσετε τις εξής εντολές ως inline τίτλους (χωρίς κουτί):
- `\Paradeigma{Τίτλος Παραδείγματος}`
- `\idiothta{Τίτλος Ιδιότητας}`
- `\protashxa{Τίτλος Πρότασης}` (δημιουργεί έγχρωμο κουτάκι)
- `\protash{Τίτλος Πρότασης}` (απλό κείμενο με εικονίδιο)

## 3. Απλά Θεωρήματα (Πανεπιστημιακά / Απλά έγγραφα)

Αν δεν θέλετε κουτιά, χρησιμοποιείτε τα κλασικά `\newtheorem`:

```latex
\newtheorem{theorem}{Θεώρημα}[section]
\newtheorem{lemma}[theorem]{Λήμμα}
\newtheorem{corollary}[theorem]{Πόρισμα}
\newtheorem{proposition}[theorem]{Πρόταση}
\newtheorem{definition}[theorem]{Ορισμός}
\newtheorem{example}{Παράδειγμα}[section]
\newtheorem{exercise}{Άσκηση}[section]
\newtheorem{remark}{Παρατήρηση}[section]

\newenvironment{solution}{\begin{proof}[Λύση]}{\end{proof}}
```

## Σχετικές σελίδες

- [[preamble]]
- [[exercise-envs]]
