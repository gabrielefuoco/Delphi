import os
import re
import sys

def remove_header_numbers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    # Regex to match headers like "## 2.1 Title", "### 2.2.1 Title"
    # It catches:
    # ^\s*          : start of line (optional whitespace)
    # (#+)          : one or more hashes (group 1)
    # \s+           : whitespace
    # (\d+(\.\d+)*) : the number part like 1, 1.1, 1.1.1 (group 2)
    # \s+           : whitespace
    # (.*)          : the rest of the title (group 4)
    header_pattern = re.compile(r'^(\s*#+)\s+\d+(?:\.\d+)*\s+(.*)')

    changes_made = False
    for line in lines:
        match = header_pattern.match(line)
        if match:
            # Reconstruct header without the number: "## Title"
            hashes = match.group(1)
            title = match.group(2)
            new_line = f"{hashes} {title}\n"
            new_lines.append(new_line)
            changes_made = True
            # print(f"Fixed: {line.strip()} -> {new_line.strip()}")
        else:
            new_lines.append(line)

    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated: {file_path}")
    return changes_made

def process_directory(root_dir):
    print(f"Scanning directory: {root_dir}")
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                if remove_header_numbers(file_path):
                    count += 1
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_header_numbers.py <project_directory>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    process_directory(project_dir)
