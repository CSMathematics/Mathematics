---
title: Module Exercise Environments
tags: [latex, module, exercises]
updated: 2026-05-08
---

# Module Exercise Environments

## Στόχος

Ενιαία δομή για φύλλα ασκήσεων, collections προβλημάτων, υποερωτήματα, λύσεις και συνοδευτικά handouts.

## Βασικό Μοτίβο

```latex
\begin{exercise}
Να λυθεί η εξίσωση ...
\begin{enumerate}[label=(\alph*)]
  \item Πρώτο ερώτημα
  \item Δεύτερο ερώτημα
\end{enumerate}
\end{exercise}

\begin{solution}
...
\end{solution}
```

## Λίστες (Λύκειο / Γυμνάσιο)

Για βοηθήματα και ασκήσεις προτείνονται οι παρακάτω λίστες του πακέτου `enumitem`:

```latex
\begin{alist}
  \item Πρώτο (a.)
  \item Δεύτερο (b.)
\end{alist}

\begin{bhma}
  \item Περιγραφή βήματος (1o Βήμα:)
\end{bhma}

\begin{tropos}
  \item Περιγραφή τρόπου (1ος Τρόπος:)
\end{tropos}

\begin{periptwsh}
  \item Περιγραφή περίπτωσης (1η Περίπτωση:)
\end{periptwsh}
```

## Ειδικές Περιπτώσεις

- Για εξετάσεις, παραμένει μόνο το scaffold των ερωτημάτων χωρίς `solution`
- Για ύφος Γ' Λυκείου μπορούν να χρησιμοποιηθούν `thema` / `erwthma` σε ξεχωριστό convention
- Οι υποδείξεις και οι σύντομες απαντήσεις ζουν σε `hint` και `answer`

## Scaffold για Θέμα Β

Για λύσεις τύπου πανελλαδικών, το προτιμώμενο pattern είναι:

```latex
\begin{thema}{Β}
Δίνεται ...
\begin{erwthma}
\item Πρώτο ερώτημα
\item Δεύτερο ερώτημα
\item Τρίτο ερώτημα
\item Τέταρτο ερώτημα
\end{erwthma}
\end{thema}
```

Κανόνες:

- Δεν παρεμβάλλεται ξεχωριστό `solution` environment μέσα στο `erwthma`
- Κάθε `\item` είναι αυτάρκης μικρο-λύση με αρχή, υπολογισμό και συμπέρασμα
- Για αναλύσεις προσήμου επιτρέπεται εσωτερικό `itemize`

## Κανόνας

Να μη συνυπάρχουν σε ίδιο αρχείο πολλαπλά ανταγωνιστικά μοτίβα αρίθμησης ασκήσεων.
