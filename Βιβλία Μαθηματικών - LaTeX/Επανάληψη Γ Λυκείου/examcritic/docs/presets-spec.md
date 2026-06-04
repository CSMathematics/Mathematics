# Presets Spec

## Active MVP preset

Το μόνο ενεργό preset για την πρώτη δοκιμή είναι:

```text
panelladikes_g_lykeiou_thema_g
```

## Preset definition

| Field | Value |
| --- | --- |
| Class | Γ΄ Λυκείου |
| Course | Μαθηματικά προσανατολισμού |
| Exam | Πανελλαδικές |
| Topic type | Θέμα Γ |
| Target difficulty | 5-7 |
| Target time | 25 minutes |
| Full time band | 22-28 minutes |
| Expected subquestions | 4 |
| Primary emphasis | Σύνθεση μεσαίας δυσκολίας και ποικιλία ύλης |

## Multipliers

| Criterion | Multiplier | Reason |
| --- | ---: | --- |
| K1 | 1.0 | Μαθηματική αρτιότητα πάντα κρίσιμη. |
| K2 | 1.0 | Η σαφήνεια δεν αλλάζει ανά preset. |
| K3 | 1.0 | Το Θέμα Γ χρειάζεται δομή, αλλά όχι απόλυτη αλυσίδα. |
| K4 | 1.5 | Η ποικιλία ύλης είναι κρίσιμη στο Θέμα Γ. |
| K5 | 1.0 | Η δυσκολία ελέγχεται από target range. |
| K6 | 1.0 | Η διδακτική αξία παραμένει σημαντική. |
| K7 | 1.0 | Ο χρόνος είναι εξεταστικός περιορισμός. |

## UI defaults

- Προεπιλογή φόρμας: Θέμα Γ.
- Προτεινόμενο target time: 25.
- Προτεινόμενο target difficulty range: 5-7.
- Προτεινόμενα branches: Ανάλυση Γ΄ Λυκείου.
- Προτεινόμενη πηγή: `Θέματα/Γ`.

## Μελλοντικά presets

Τα παρακάτω μένουν ανενεργά μέχρι να γίνει calibration:

- `panelladikes_g_lykeiou_thema_a`
- `panelladikes_g_lykeiou_thema_b`
- `panelladikes_g_lykeiou_thema_d`
- `internal_exam_g_lykeiou_medium`
- `homework_g_lykeiou_weekly`

