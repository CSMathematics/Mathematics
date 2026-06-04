# LLM Wiki — Μαθηματικά & LaTeX

Προσωπική βάση γνώσης που συντηρεί ο Claude Code.
Χρήση μέσω Obsidian (graph view) και Google Drive agent.

---

## Σκοπός

Οργανωμένες σημειώσεις, ασκήσεις και βιβλία Μαθηματικών σε LaTeX.
Το wiki εξυπηρετεί τρεις ρόλους:
1. Προσωπική οργάνωση (Obsidian)
2. Οδηγίες LaTeX για AI agents
3. Token-efficient context για κάθε εργασία

---

## Folder Structure

```
raw/                    -- πηγές (αμετάβλητες — μην τροποποιείς)
wiki/
  index.md              -- πίνακας περιεχομένων
  log.md                -- append-only ιστορικό αλλαγών
  math/                 -- concept pages ανά κλάδο
  latex/                -- LaTeX templates & προδιαγραφές
  conventions/          -- συμβάσεις σημειογραφίας
templates/              -- .tex αρχεία-βάση ανά τύπο εγγράφου
```

---

## Κλάδοι Μαθηματικών

`gymnasium` | `lykeio` | `analysis` | `algebra` | `geometry`
`statistics` | `probability` | `ode` | `complex-analysis`

Κάθε concept page ανήκει σε έναν ή περισσότερους κλάδους (frontmatter: `branches:`).

---

## Τύποι Εγγράφων

| Τύπος | Tag | Περιγραφή |
|-------|-----|-----------|
| Ασκήσεις με λύσεις | `exercises` | Numbered, με \begin{solution} |
| Θεωρητικές σημειώσεις | `notes` | Θεωρήματα, αποδείξεις, ορισμοί |
| Βιβλίο / σύγγραμμα | `book` | Chapters, sections, index |
| Εξέταση / διαγώνισμα | `exam` | Χωρίς λύσεις, με μόρια |

---

## LaTeX Προδιαγραφές

### Γενικοί κανόνες (ΠΑΝΤΑ)

- Encoding: `\usepackage[utf8]{inputenc}` + `\usepackage[greek,english]{babel}`
- Fonts: `\usepackage{amsmath, amssymb, amsthm, mathtools}`
- Geometry: `\usepackage[a4paper, margin=2.5cm]{geometry}`
- Hyperlinks: `\usepackage[hidelinks]{hyperref}`
- Γλώσσα: Ελληνικά εκτός αν ζητηθεί αλλιώς

### Μαθηματικά περιβάλλοντα

```latex
% Θεώρημα / Λήμμα / Πόρισμα / Ορισμός
\newtheorem{theorem}{Θεώρημα}[section]
\newtheorem{lemma}[theorem]{Λήμμα}
\newtheorem{corollary}[theorem]{Πόρισμα}
\newtheorem{definition}[theorem]{Ορισμός}
\newtheorem{example}{Παράδειγμα}[section]
\newtheorem{exercise}{Άσκηση}[section]

% Απόδειξη — χρήση \begin{proof}...\end{proof}
% Λύση — χρήση \begin{solution}...\end{solution} (custom)
\newenvironment{solution}{\begin{proof}[Λύση]}{\end{proof}}
```

### Σημειογραφία ανά κλάδο

**Ανάλυση**
- Όρια: `\lim_{x \to a}`, όχι `lim`
- Παράγωγος: `f'(x)` ή `\frac{df}{dx}` — συνέπεια εντός εγγράφου
- Ολοκλήρωμα: `\int_a^b f(x)\,dx` (με `\,` πριν το `dx`)
- Σύνολα: `\mathbb{R}`, `\mathbb{N}`, `\mathbb{Z}`, `\mathbb{Q}`, `\mathbb{C}`

**Άλγεβρα**
- Διανύσματα: `\mathbf{v}` ή `\vec{v}` — ένα μόνο ανά έγγραφο
- Πίνακες: `\begin{pmatrix}...\end{pmatrix}` (στρογγυλές)
- Ορίζουσα: `\det(A)` ή `|A|`

**Γεωμετρία**
- Γωνία: `\angle ABC`, μοίρες: `30°` ή `30^\circ`
- Απόσταση: `|AB|` ή `d(A,B)`

**Στατιστική / Πιθανότητες**
- `P(A)`, `E[X]`, `\text{Var}(X)`, `\sigma^2`
- Κατανομές: `X \sim \mathcal{N}(\mu, \sigma^2)`

**Διαφορικές Εξισώσεις**
- `y' + p(x)y = q(x)` (Lagrange notation για ODE 1ης τάξης)
- `\frac{d^2y}{dx^2}` για ανώτερης τάξης

**Μιγαδική Ανάλυση**
- `z = a + bi`, `\bar{z}`, `|z|`, `\text{Re}(z)`, `\text{Im}(z)`
- `e^{i\theta} = \cos\theta + i\sin\theta`

### Επίπεδο δυσκολίας

Ο agent πρέπει να γνωρίζει το επίπεδο πριν γράψει:

| Επίπεδο | Tag | Χαρακτηριστικά |
|---------|-----|----------------|
| Γυμνάσιο | `gym` | Απλή γλώσσα, χωρίς αποδείξεις |
| Λύκειο | `lyk` | Ορισμοί + εφαρμογές, ελάχιστη θεωρία |
| Προπτυχιακό | `bsc` | Πλήρεις αποδείξεις, αυστηρή σημειογραφία |
| Μεταπτυχιακό/Έρευνα | `msc` | Αφηρημένη θεωρία, γενικευμένα αποτελέσματα |

---

## Ingest Workflow

Όταν ο χρήστης προσθέτει πηγή στο `raw/`:

1. Διάβασε το πλήρες έγγραφο
2. Συζήτησε τα κύρια σημεία πριν γράψεις οτιδήποτε
3. Δημιούργησε summary page στο `wiki/`
4. Δημιούργησε/ενημέρωσε concept pages για κάθε κύρια ιδέα
5. Πρόσθεσε wiki-links ([[page-name]]) για συνδέσεις
6. Ενημέρωσε `wiki/index.md`
7. Προσάρτησε εγγραφή στο `wiki/log.md`

---

## Page Format

```markdown
---
title: Τίτλος Σελίδας
branches: [analysis, algebra]   # κλάδοι
level: [bsc, msc]               # επίπεδο
tags: [theorem, definition]     # τύπος περιεχομένου
sources: [filename.pdf]
updated: YYYY-MM-DD
---

# Τίτλος Σελίδας

**Σύνοψη**: Μία-δύο προτάσεις.

**Πηγές**: raw/filename.pdf

---

Κύριο περιεχόμενο. Σύνδεσμοι σε σχετικές έννοιες: [[related-concept]].

## Σχετικές σελίδες

- [[related-concept-1]]
- [[related-concept-2]]
```

---

## Citation Rules

- Κάθε ισχυρισμός: `(πηγή: filename.pdf)`
- Αντίφαση μεταξύ πηγών: σημείωσε ρητά
- Χωρίς πηγή: `⚠️ χρειάζεται επαλήθευση`

---

## Question Answering

1. Διάβασε `wiki/index.md` για σχετικές σελίδες
2. Διάβασε τις σελίδες και συνθέτα απάντηση
3. Παράπεμψε σε συγκεκριμένες wiki σελίδες
4. Αν δεν υπάρχει απάντηση στο wiki: πες το καθαρά
5. Αν η απάντηση είναι χρήσιμη: πρότεινε να αποθηκευτεί ως νέα σελίδα

---

## LaTeX Agent Instructions

Όταν ο agent γράφει .tex αρχείο:

1. **Ρώτα πρώτα** (αν δεν είναι δηλωμένο): τύπος εγγράφου + επίπεδο + κλάδος
2. **Διάβασε** το αντίστοιχο template από `templates/`
3. **Ακολούθησε** τις σημειογραφίες από το `wiki/conventions/`
4. **Μην εφευρίσκεις** νέες συμβάσεις — αν λείπει κάτι, ρώτα
5. **Compile check**: κάθε .tex να είναι compilable χωρίς errors

### Token-efficient context

Όταν ξεκινάς νέα εργασία LaTeX, φόρτωσε μόνο:
- `wiki/latex/[branch]-conventions.md`
- `templates/[doctype].tex` (preamble μόνο)
- `wiki/index.md` (για links)

Όχι ολόκληρο το wiki.

---

## Lint

Έλεγξε για:
- Αντιφάσεις μεταξύ σελίδων
- Orphan pages (χωρίς inbound links)
- Έννοιες χωρίς δική τους σελίδα
- Σελίδες εκτός format
- LaTeX conventions που διαφέρουν μεταξύ σελίδων

Αποτέλεσμα: αριθμημένη λίστα με προτεινόμενες διορθώσεις.

---

## Rules

- **Ποτέ** μην τροποποιείς το `raw/`
- **Πάντα** ενημέρωσε `wiki/index.md` και `wiki/log.md` μετά από αλλαγές
- Ονόματα σελίδων: lowercase με hyphens (`πχ. riemann-integral.md`)
- Γλώσσα wiki: Ελληνικά (εκτός LaTeX code)
- Αν αμφιβάλλεις για κατηγοριοποίηση: ρώτα
- LaTeX: προτίμησε `\[...\]` αντί `$$...$$` για display math
