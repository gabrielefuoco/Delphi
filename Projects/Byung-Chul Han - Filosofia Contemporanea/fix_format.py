import os
import shutil
import re

base_dir = r"c:\Users\gabri\APP\Apprendimento 2.0\Delphi\Projects\Byung-Chul Han - Filosofia Contemporanea\chapters"
chunks_file = r"c:\Users\gabri\APP\Apprendimento 2.0\Delphi\Projects\Byung-Chul Han - Filosofia Contemporanea\chunks.txt"

with open(chunks_file, 'r', encoding='utf-8') as f:
    titles = [line.strip() for line in f if line.strip()]

# Remove old 01_Capitolo 1
old_dir = os.path.join(base_dir, "01_Capitolo 1")
if os.path.exists(old_dir):
    shutil.rmtree(old_dir)

# Now we should have 10 directories left, from 02_Capitolo 1 to 11_Capitolo 10
dirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])

for i, d in enumerate(dirs):
    title = titles[i]
    old_path = os.path.join(base_dir, d)
    # create new safe name
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    new_dir_name = f"{i+1:02d}_{safe_title}"
    new_path = os.path.join(base_dir, new_dir_name)
    
    os.rename(old_path, new_path)
    
    # fix the markdown file
    md_file = None
    for f in os.listdir(new_path):
        if f.endswith('.md'):
            md_file = os.path.join(new_path, f)
            break
            
    if md_file:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Add heading if not present
        if not content.startswith(f"# {title}"):
            content = f"# {title}\n\n" + content
            
        # Fix bulleted lists: find lines starting with '* ' and ensure there's a blank line before them
        # And change '* ' to '- '
        lines = content.split('\n')
        new_lines = []
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('* '):
                # if the previous line is not empty and not another list item, add a blank line
                if len(new_lines) > 0 and new_lines[-1].strip() != '' and not new_lines[-1].strip().startswith('- '):
                    new_lines.append('')
                # preserve indentation if any
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(indent + '- ' + stripped[2:])
            else:
                new_lines.append(line)
                
        content = '\n'.join(new_lines)
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fix completed.")
