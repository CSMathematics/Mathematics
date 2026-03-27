import re

with open('trapeza_AL_algebra.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Check alist formatting
pattern1 = re.compile(r'(\\Askhsh\{\[([0-9]+)\]\})(\s*)(\\begin\{alist\})')
matches1 = pattern1.findall(text)
print(f"Found {len(matches1)} instances where \\Askhsh is immediately followed by \\begin{{alist}}")

# 2. Check tikzpictures
# Let's find all \Askhsh and \begin{tikzpicture}...\end{tikzpicture}
# A simple regex for tikzpicture (assuming no nested tikzpictures):
tikz_pattern = re.compile(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', re.DOTALL)
tikz_blocks = list(tikz_pattern.finditer(text))
print(f"Found {len(tikz_blocks)} tikzpictures.")

askhsh_pattern = re.compile(r'\\Askhsh\{\[([0-9]+)\]\}')
askhsh_blocks = list(askhsh_pattern.finditer(text))

# For each tikzpicture, let's find the most recent Askhsh ID
# and check if caption follows or precedes.
# We will check a window of text around the tikzpicture.
no_caption_count = 0
for tikz in tikz_blocks:
    start, end = tikz.span()
    
    # find most recent Askhsh
    last_askhsh = None
    for a in reversed(askhsh_blocks):
        if a.start() < start:
            last_askhsh = a.group(1)
            break
            
    # Check for caption or captionof within 150 chars after the end of the tikz block
    # Or before the start of the tikz block. Often captions are just after.
    # Let's check the enclosing environment. Usually \begin{figure} ... \end{figure} or marginfigure
    # Let's check 300 characters around the picture:
    window_start = max(0, start - 200)
    window_end = min(len(text), end + 200)
    window = text[window_start:window_end]
    
    if '\\caption' not in window:
        no_caption_count += 1

print(f"Found {no_caption_count} tikzpictures without \\caption or \\captionof nearby.")
