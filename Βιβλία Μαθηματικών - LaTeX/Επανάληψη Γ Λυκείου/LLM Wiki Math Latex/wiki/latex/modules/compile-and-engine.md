---
title: Module Compile and Engine Policy
tags: [latex, module, compile]
updated: 2026-05-08
---

# Module Compile and Engine Policy

## Προεπιλογή

- Default engine: `pdflatex`
- Default στόχος: compilable αρχεία χωρίς errors
- Αν απαιτούνται system fonts ή σύγχρονο unicode workflow, επιτρέπεται `xelatex`, αλλά πρέπει να δηλώνεται ρητά

## Κανόνες

- Το template πρέπει να μπορεί να γίνει compile μόνο του
- Να αποφεύγονται σπάνια packages χωρίς σαφή ανάγκη
- Όταν προστίθενται TikZ ή `pgfplots`, να ελέγχεται ότι τα imports είναι πλήρη
- Να μην υπάρχουν unresolved references ή environment mismatches

## Ελάχιστος Έλεγχος

1. Compile χωρίς fatal error
2. Έλεγχος για undefined control sequences
3. Έλεγχος για unclosed environments
4. Έλεγχος ότι οι ελληνικοί χαρακτήρες αποδίδονται σωστά στο επιλεγμένο engine
