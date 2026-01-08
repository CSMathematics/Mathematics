import sys
import os

print("Script starting...")
filename = '/home/spyros/Μαθηματικά/Φροντιστήριο ΦΙΛΟΜΑΘΕΙΑ/Γ΄ Λυκείου/Μαθηματικά προσανατολισμού/Ασκήσεις/DTX-Epanalipsi_meleth_synarthshs.tex'

if not os.path.exists(filename):
    print(f"File not found: {filename}")
    sys.exit(1)

try:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"Read {len(lines)} lines.")
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

stack = []
for line_idx, line in enumerate(lines):
    # Remove comments
    clean_line = ""
    i = 0
    while i < len(line):
        if line[i] == '%':
            if i > 0 and line[i-1] == '\\':
                clean_line += '%'
            else:
                break 
        else:
            clean_line += line[i]
        i += 1
        
    j = 0
    while j < len(clean_line):
        char = clean_line[j]
        if char == '\\':
            j += 2
            continue
        if char == '{':
            stack.append((line_idx + 1, j + 1))
        elif char == '}':
            if not stack:
                print(f"Extra closing brace '}}' at Line {line_idx+1}, Col {j+1}")
            else:
                stack.pop()
        j += 1

if stack:
    print("Unclosed braces:")
    for (l, c) in stack:
        print(f"  Line {l}, Col {c}")
else:
    print("No brace mismatch found.")
