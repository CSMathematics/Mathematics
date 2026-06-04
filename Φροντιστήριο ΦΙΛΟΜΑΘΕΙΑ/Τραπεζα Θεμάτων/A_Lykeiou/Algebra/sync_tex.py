import os
import re

def sync_files():
    final_tex_path = '/home/spyros/Μαθηματικά/Φροντιστήριο ΦΙΛΟΜΑΘΕΙΑ/Τραπεζα Θεμάτων/A_Lykeiou/Algebra/output_tex/trapeza_AL_algebra_sections.tex'
    output_tex_dir = '/home/spyros/Μαθηματικά/Φροντιστήριο ΦΙΛΟΜΑΘΕΙΑ/Τραπεζα Θεμάτων/A_Lykeiou/Algebra/output_tex'
    output_sol_dir = '/home/spyros/Μαθηματικά/Φροντιστήριο ΦΙΛΟΜΑΘΕΙΑ/Τραπεζα Θεμάτων/A_Lykeiou/Algebra/output_solutions'
    
    with open(final_tex_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_files = 0
    missing_files = 0

    current_block_type = None
    current_ex_id = None
    current_content = []
    
    def save_current_block():
        nonlocal updated_files, missing_files
        if current_block_type and current_ex_id and current_content:
            # clean up trailing empty lines and \vspace{4mm}
            while current_content and current_content[-1].strip() == '':
                current_content.pop()
            if current_content and current_content[-1].strip() == r'\vspace{4mm}':
                current_content.pop()
            while current_content and current_content[-1].strip() == '':
                current_content.pop()
                
            block_text = "".join(current_content) + "\n"
            
            if current_block_type == 'Άσκηση':
                filename = f"{current_ex_id}.tex"
                filepath = os.path.join(output_tex_dir, filename)
            elif current_block_type == 'Λύση':
                filename = f"{current_ex_id}_solution.tex"
                filepath = os.path.join(output_sol_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as out_f:
                    out_f.write(block_text)
                print(f"Updated {filepath}")
                updated_files += 1
            else:
                print(f"Warning: File {filepath} does not exist. Skipping.")
                missing_files += 1

    pattern = re.compile(r'^% --- (Άσκηση|Λύση) (\d+) \([^)]+\) ---')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            # Save previous block
            save_current_block()
            
            # Start new block
            current_block_type = match.group(1)
            current_ex_id = match.group(2)
            current_content = []
        elif line.startswith(r'\chapter{'):
            # Save previous block and stop collecting
            save_current_block()
            current_block_type = None
            current_ex_id = None
            current_content = []
        elif current_block_type:
            current_content.append(line)
            
    # Save the last block
    save_current_block()

    print(f"\nDone! Updated {updated_files} files. {missing_files} files were missing.")

if __name__ == '__main__':
    sync_files()
