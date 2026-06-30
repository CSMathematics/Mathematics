#!/usr/bin/env python3
r"""
Python script to merge individual LaTeX solution files (e.g. solution_A_*.tex)
from a subfolder in 'Λύσεις θεμάτων' into a single combined LaTeX file.
It extracts and deduplicates command definitions (e.g. \providecommand blocks)
so they are only declared once at the top of the output file.
"""

import os
import re
import argparse

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def main():
    parser = argparse.ArgumentParser(description="Merge LaTeX solutions and deduplicate commands.")
    parser.add_argument(
        "--folder",
        default="Α",
        help="Subfolder in 'Λύσεις θεμάτων' to merge (e.g., Α, Β, Γ, Δ)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output filepath. Defaults to 'Λύσεις θεμάτων/<folder>/merged_solutions_<folder>.tex'"
    )
    args = parser.parse_args()

    base_dir = "/home/spyros/Μαθηματικά/Βιβλία Μαθηματικών - LaTeX/Επανάληψη Γ Λυκείου"
    solutions_dir = os.path.join(base_dir, "Λύσεις θεμάτων", args.folder)

    if not os.path.isdir(solutions_dir):
        print(f"Error: Directory not found: {solutions_dir}")
        return

    # Find all .tex files matching solution_*.tex
    files = [f for f in os.listdir(solutions_dir) if f.startswith("solution_") and f.endswith(".tex")]
    files.sort(key=natural_sort_key)

    if not files:
        print(f"No solution files found in {solutions_dir}")
        return

    print(f"Found {len(files)} solution files to merge.")

    unique_definitions = []
    seen_definitions = set()
    merged_body_parts = []

    for file_name in files:
        file_path = os.path.join(solutions_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Parse the file lines to locate the solution body start
        body_start_idx = None
        for idx, line in enumerate(lines):
            if r"\begin{thema}" in line:
                body_start_idx = idx
                break

        if body_start_idx is None:
            print(f"Warning: '\\begin{{thema}}' not found in {file_name}. Including whole file as body.")
            merged_body_parts.append(([], "".join(lines)))
            continue

        # Separate header comments/whitespace from command definitions
        header_lines = []
        def_lines = []
        for i in range(body_start_idx):
            line = lines[i]
            if line.strip().startswith("%"):
                # If we haven't started collecting definitions yet, this is a header comment
                if not def_lines:
                    header_lines.append(line)
                else:
                    def_lines.append(line)
            elif line.strip() == "":
                if def_lines:
                    def_lines.append(line)
                else:
                    header_lines.append(line)
            else:
                def_lines.append(line)

        # Deduplicate command definition block
        def_str = "".join(def_lines).strip()
        if def_str:
            normalized_def = re.sub(r"\s+", " ", def_str).strip()
            if normalized_def not in seen_definitions:
                seen_definitions.add(normalized_def)
                unique_definitions.append(def_str)

        # Body consists of everything from body_start_idx to the end
        body_str = "".join(lines[body_start_idx:])
        merged_body_parts.append((header_lines, body_str))

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(solutions_dir, f"merged_solutions_{args.folder}.tex")

    # Generate merged contents
    with open(output_path, "w", encoding="utf-8") as f:
        # Write unique definitions first
        if unique_definitions:
            f.write("%=========== ΚΟΙΝΕΣ ΕΝΤΟΛΕΣ ===========\n")
            for definition in unique_definitions:
                f.write(definition + "\n")
            f.write("%======================================\n\n")

        # Write each solution's body
        for idx, (header_lines, body_str) in enumerate(merged_body_parts):
            if header_lines:
                f.writelines(header_lines)
            f.write(body_str)
            if not body_str.endswith("\n"):
                f.write("\n")
            f.write("\n")

    print(f"Successfully merged into: {output_path}")

if __name__ == "__main__":
    main()
