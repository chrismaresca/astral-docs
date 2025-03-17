#!/usr/bin/env python3
import sys
import subprocess
import re
import os

def get_last_modified(file_path):
    try:
        output = subprocess.check_output(["git", "log", "-1", "--format=%ci", file_path], encoding="utf-8")
        return output.strip()
    except subprocess.CalledProcessError:
        return None

def infer_version(file_path):
    # Assumes the structure: docs/<version>/...
    parts = file_path.split(os.sep)
    try:
        docs_index = parts.index("docs")
        return parts[docs_index + 1]
    except (ValueError, IndexError):
        return ""

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    last_mod = get_last_modified(file_path)
    version = infer_version(file_path)
    if not last_mod:
        print(f"Could not determine last modified time for {file_path}")
        return False

    updated = False

    # Update or insert lastUpdated field.
    last_updated_pattern = re.compile(r'(lastUpdated:\s*").*?(")')
    new_last_updated_line = f'lastUpdated: "{last_mod}"'
    if last_updated_pattern.search(content):
        new_content, count = last_updated_pattern.subn(new_last_updated_line, content)
        if count > 0:
            content = new_content
            updated = True
    else:
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                rest = parts[2]
                frontmatter += f'\n{new_last_updated_line}\n'
                content = f'---{frontmatter}---{rest}'
                updated = True

    # Update or insert version field.
    version_pattern = re.compile(r'(version:\s*").*?(")')
    new_version_line = f'version: "{version}"'
    if version_pattern.search(content):
        new_content, count = version_pattern.subn(new_version_line, content)
        if count > 0:
            content = new_content
            updated = True
    else:
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                rest = parts[2]
                frontmatter += f'\n{new_version_line}\n'
                content = f'---{frontmatter}---{rest}'
                updated = True

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated metadata for {file_path}")
    return updated

if __name__ == "__main__":
    modified_files = sys.argv[1:]
    updated_any = False
    for file_path in modified_files:
        if update_file(file_path):
            updated_any = True
    if updated_any:
        print("One or more files were updated.")
    else:
        print("No files were updated.")
