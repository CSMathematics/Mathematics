# Scoring Formulas

## Base criterion scores

Κάθε κριτήριο παράγει raw score στο δικό του μέγιστο:

| Criterion | Max |
| --- | ---: |
| K1 | 15 |
| K2 | 10 |
| K3 | 10 |
| K4 | 20 |
| K5 | 15 |
| K6 | 20 |
| K7 | 10 |

Το base total είναι 100 πριν εφαρμοστεί preset multiplier.

## K3 conversion

```text
K3 = 2 * K3.1_raw + 2 * K3.2_raw + K3.3_raw
```

Όπου κάθε raw τιμή είναι 0, 1 ή 2.

## Raw difficulty

```text
RD = (
  2 * technical_complexity +
  2 * conceptual_depth +
  1 * solution_steps +
  1 * originality
) / 6
```

Κάθε παράγοντας είναι 0-10. Το αποτέλεσμα `RD` είναι 0-10.

## Difficulty score for Θέμα Γ

Target range: 5-7.

```text
if 5 <= RD <= 7:
  K5 = 15
else:
  distance = min(abs(RD - 5), abs(RD - 7))
  K5 = clamp(15 - 3 * distance, 0, 15)
```

Αυτό διορθώνει τη σύγκρουση ανάμεσα σε midpoint scoring και target range: όλο το εύρος 5-7 θεωρείται επιτυχές για Θέμα Γ.

## Time score for Θέμα Γ

Target time: 25 minutes. Full-score band: 22-28 minutes.

```text
if 22 <= estimated_minutes <= 28:
  K7 = 10
else:
  nearest = 22 if estimated_minutes < 22 else 28
  distance_ratio = abs(estimated_minutes - nearest) / 25
  K7 = clamp(10 - 20 * distance_ratio, 0, 10)
```

Παράδειγμα:

- 25 λεπτά: 10/10
- 18 λεπτά: 6.8/10
- 35 λεπτά: 4.4/10

## Preset multiplier and normalization

Το Γ Θέμα δίνει μεγαλύτερη σημασία στην κάλυψη ύλης.

```text
effective_weight[K] = base_weight[K] * preset_multiplier[K]
normalized_weight[K] = 100 * effective_weight[K] / sum(effective_weights)
criterion_ratio[K] = raw_score[K] / base_weight[K]
final_score = sum(criterion_ratio[K] * normalized_weight[K])
```

Για το MVP, μόνο το Κ4 έχει multiplier 1.5.

Effective weights:

| Criterion | Base | Multiplier | Effective | Normalized |
| --- | ---: | ---: | ---: | ---: |
| K1 | 15 | 1.0 | 15 | 13.64 |
| K2 | 10 | 1.0 | 10 | 9.09 |
| K3 | 10 | 1.0 | 10 | 9.09 |
| K4 | 20 | 1.5 | 30 | 27.27 |
| K5 | 15 | 1.0 | 15 | 13.64 |
| K6 | 20 | 1.0 | 20 | 18.18 |
| K7 | 10 | 1.0 | 10 | 9.09 |

## Score bands

| Score | Label | Meaning |
| ---: | --- | --- |
| 90-100 | Εξαιρετικό | Μπορεί να λειτουργήσει ως πρότυπο θέμα. |
| 75-89 | Πολύ καλό | Θέλει μόνο μικρές βελτιώσεις. |
| 60-74 | Αποδεκτό | Χρήσιμο, αλλά χρειάζεται αναθεώρηση. |
| 40-59 | Προβληματικό | Έχει σημαντικά ζητήματα δομής, δυσκολίας ή σαφήνειας. |
| 0-39 | Ακατάλληλο | Δεν πρέπει να χρησιμοποιηθεί χωρίς ουσιαστική επανεγγραφή. |

