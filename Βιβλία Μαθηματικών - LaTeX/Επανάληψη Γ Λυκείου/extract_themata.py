#!/usr/bin/env python3
"""
Extracts individual exercise LaTeX files for each \begin{thema}{X}...\end{thema} block
across all 4 sections of Epanalipsi_G_Lykeioy.tex.

Output structure:
  Θέματα/Α/thema_A_01.tex  (Θέματα Α)
  Θέματα/Β/thema_B_01.tex  (Θέματα Β)
  Θέματα/Γ/thema_G_01.tex  (Θέματα Γ)
  Θέματα/D/thema_D_01.tex  (Θέματα Δ)

No preamble is included – only the raw exercise content between
\begin{thema}{X} and \end{thema}.
"""

import os

# ---- Source file ----
BASE_DIR = "/home/spyros/Μαθηματικά/Βιβλία Μαθηματικών - LaTeX/Επανάληψη Γ Λυκείου"
FILEPATH = os.path.join(BASE_DIR, "themata_C.tex")

# ---- Section definitions ----
# Each entry: (SECTION_TITLE, THEMA_LETTER, FOLDER_NAME, FILE_PREFIX)
SECTIONS = [
    # ("Θέματα Α", "A",  "Α", "thema_A"),   # Latin A
    # ("Θέματα Β", "Β",  "Β", "thema_B"),   # Latin B
    ("Θέματα Γ", "Γ",  "Γ", "thema_G"),   # Greek Γ
    # ("Θέματα Δ", "Δ",  "Δ", "thema_D"),   # Greek Δ
]

# ---- Output base directory ----
OUTPUT_BASE = os.path.join(BASE_DIR, "Θέματα")

# ====================================================================

with open(FILEPATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Loaded {len(lines)} lines from file.")

# --- Find section boundaries ---
# Map section_title -> start_line_index
section_starts = {}
section_order  = []

for i, line in enumerate(lines):
    stripped = line.strip()
    for (title, letter, folder, prefix) in SECTIONS:
        if stripped == r'\section{' + title + '}':
            section_starts[title] = i
            section_order.append(title)

# Determine end of each section (= start of next section, or EOF)
section_ends = {}
for idx, title in enumerate(section_order):
    if idx + 1 < len(section_order):
        section_ends[title] = section_starts[section_order[idx + 1]]
    else:
        section_ends[title] = len(lines)

print("\nSection boundaries:")
for title in section_order:
    print(f"  '{title}': lines {section_starts[title]+1} – {section_ends[title]}")

# --- Extract and write individual thema files ---
total_written = 0

for (section_title, thema_letter, folder_name, file_prefix) in SECTIONS:
    if section_title not in section_starts:
        print(f"\nWARNING: Section '{section_title}' not found – skipping.")
        continue

    start = section_starts[section_title]
    end   = section_ends[section_title]

    begin_marker = r'\begin{thema}{' + thema_letter + '}'
    end_marker   = r'\end{thema}'

    # Create output folder
    out_dir = os.path.join(OUTPUT_BASE, folder_name)
    os.makedirs(out_dir, exist_ok=True)

    # Find all (begin_idx, end_idx) pairs
    pairs = []
    i = start
    while i < end:
        if lines[i].strip() == begin_marker:
            begin_idx = i
            # Find matching \end{thema}
            j = i + 1
            while j < end:
                if lines[j].strip() == end_marker:
                    pairs.append((begin_idx, j))
                    i = j  # continue scanning from end{thema}
                    break
                j += 1
            else:
                print(f"  WARNING: No matching \\end{{thema}} for begin at line {begin_idx+1}")
        i += 1

    print(f"\n'{section_title}': found {len(pairs)} exercises → {out_dir}")

    # Write each exercise to its own file
    for idx_pair, (begin_idx, end_idx) in enumerate(pairs):
        n = idx_pair + 1
        filename = f"{file_prefix}_{n:02d}.tex"
        filepath_out = os.path.join(out_dir, filename)

        # Content = everything from \begin{thema}{X} to \end{thema} (inclusive)
        content_lines = lines[begin_idx : end_idx + 1]
        content = ''.join(content_lines)

        with open(filepath_out, 'w', encoding='utf-8') as fout:
            fout.write(content)

        total_written += 1

    print(f"  Written {len(pairs)} files.")

print(f"\nDone! Total files written: {total_written}")
print(f"Output directory: {OUTPUT_BASE}")
