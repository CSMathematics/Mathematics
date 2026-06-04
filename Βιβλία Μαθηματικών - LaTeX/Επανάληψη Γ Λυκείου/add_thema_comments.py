#!/usr/bin/env python3
"""
Adds comments before \begin{thema}{B} and after the matching \end{thema}
in the Θέματα Β section of the LaTeX file.

Usage:
    python3 add_thema_comments.py

Set THEMA_LETTER and SECTION_TITLE to adapt for other sections (Γ, Δ, ...).
"""

filepath = "/home/spyros/Μαθηματικά/Βιβλία Μαθηματικών - LaTeX/Επανάληψη Γ Λυκείου/Epanalipsi_G_Lykeioy.tex"

# ---- Configuration ----
THEMA_LETTER   = "Δ"           # The letter inside \begin{thema}{...}   (Latin A/B/C/D)
COMMENT_LETTER = "Δ"           # The Greek letter for the comment text   (Α/Β/Γ/Δ)
SECTION_TITLE  = "Θέματα Δ"   # The title of the \section{} to search within
# -----------------------

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")

# --- Step 1: Find the start index of the target section ---
section_start_idx = None
next_section_idx  = None

begin_marker = r'\begin{thema}{' + THEMA_LETTER + '}'
end_marker   = r'\end{thema}'

for i, line in enumerate(lines):
    stripped = line.strip()
    if section_start_idx is None:
        # Look for our section header
        if stripped == r'\section{' + SECTION_TITLE + '}':
            section_start_idx = i
    else:
        # Look for the next section/part/chapter to know where to stop
        if (stripped.startswith(r'\section{') or
                stripped.startswith(r'\part{') or
                stripped.startswith(r'\chapter{')):
            next_section_idx = i
            break

if section_start_idx is None:
    raise ValueError(f"Section '\\section{{{SECTION_TITLE}}}' not found in file!")

print(f"Section '{SECTION_TITLE}' found at line {section_start_idx + 1}")
if next_section_idx:
    print(f"Next section found at line {next_section_idx + 1}")
else:
    next_section_idx = len(lines)
    print("No next section found; searching to end of file.")

# --- Step 2: Collect (begin_idx, end_idx) pairs for \begin{thema}{LETTER} blocks ---
# Strategy: for each \begin{thema}{LETTER} found, the VERY NEXT \end{thema} is its pair.
pairs = []  # list of (begin_idx, end_idx)

i = section_start_idx
while i < next_section_idx:
    if lines[i].strip() == begin_marker:
        begin_idx = i
        # Find the matching \end{thema}
        j = i + 1
        while j < next_section_idx:
            if lines[j].strip() == end_marker:
                pairs.append((begin_idx, j))
                i = j  # continue scanning from end{thema} onwards
                break
            j += 1
        else:
            raise ValueError(f"No matching \\end{{thema}} found for \\begin{{thema}}{{{THEMA_LETTER}}} at line {begin_idx + 1}")
    i += 1

print(f"Found {len(pairs)} \\begin{{thema}}{{{THEMA_LETTER}}} / \\end{{thema}} pairs")

# --- Step 3: Build insertion list (process from bottom to top to preserve indices) ---
insertions = []  # list of (line_idx, 'before'|'after', comment_text)

for idx_pair, (begin_idx, end_idx) in enumerate(pairs):
    n = idx_pair + 1  # 1-indexed theme number
    begin_comment = f"%=========== {n}ο ΘΕΜΑ {COMMENT_LETTER} ===========\n"
    end_comment   = f"%=========== ΤΕΛΟΣ - {n}ο ΘΕΜΑ {COMMENT_LETTER} ===========\n"
    insertions.append((begin_idx, 'before', begin_comment))
    insertions.append((end_idx,   'after',  end_comment))

# Sort descending by line index; for same line, 'after' before 'before'
insertions.sort(key=lambda x: (x[0], 0 if x[1] == 'after' else 1), reverse=True)

# --- Step 4: Insert comments ---
new_lines = list(lines)

for (idx, position, comment) in insertions:
    if position == 'before':
        new_lines.insert(idx, comment)
    else:  # 'after'
        new_lines.insert(idx + 1, comment)

print(f"\nOriginal lines : {len(lines)}")
print(f"New lines      : {len(new_lines)}")
print(f"Difference     : {len(new_lines) - len(lines)}  (expected {len(pairs) * 2})")

# --- Step 5: Write back ---
with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("\nDone! File written successfully.")
