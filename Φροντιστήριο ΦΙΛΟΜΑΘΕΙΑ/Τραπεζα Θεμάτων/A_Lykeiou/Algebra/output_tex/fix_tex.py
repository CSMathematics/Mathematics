import re
import sys

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Substitute \Askhsh{[ID]} immediately followed by \begin{alist}
    # It will find instances with whitespace/newlines in between and add \vspace{-5mm} BEFORE \begin{alist}
    pattern_alist = re.compile(r'(\\Askhsh\{\[([0-9]+)\]\})(\s*)(\\begin\{alist\})')
    content = pattern_alist.sub(r'\1\3\\vspace{-5mm}\n\4', content)

    # 2. Add \captionof{figure}{Άσκηση <κωδικός>} to tikzpictures lacking captions
    askhsh_pattern = re.compile(r'\\Askhsh\{\[([0-9]+)\]\}')
    tikz_pattern = re.compile(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', re.DOTALL)
    
    askhsh_positions = [(m.start(), m.group(1)) for m in askhsh_pattern.finditer(content)]
    tikz_blocks = list(tikz_pattern.finditer(content))
    
    new_content = content
    # Process from back to front to avoid index shifting problems
    for tikz in reversed(tikz_blocks):
        start, end = tikz.span()
        
        # Find corresponding Exercise ID
        current_id = None
        for a_pos, a_id in reversed(askhsh_positions):
            if a_pos < start:
                current_id = a_id
                break
                
        if not current_id:
            continue
            
        # Check if caption is nearby (150 chars before or after)
        before_window = content[max(0, start-150):start]
        after_window = content[end:end+150]
        
        if '\\caption' not in before_window and '\\caption' not in after_window:
            insertion_text = f"\n\\captionof{{figure}}{{Άσκηση {current_id}}}\n"
            new_content = new_content[:end] + insertion_text + new_content[end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Modifications successfully applied.")

if __name__ == "__main__":
    process_file('/home/spyros/Μαθηματικά/Τράπεζα Θεμάτων/1_1_5/output_tex/trapeza_AL_algebra.tex')
