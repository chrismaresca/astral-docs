#!/usr/bin/env python3
# -------------------------------------------------------------------------------- #
# Last Updated Metadata Updater
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
import sys
import subprocess
import re
import os

# -------------------------------------------------------------------------------- #
# Helper Functions
# -------------------------------------------------------------------------------- #
def get_last_modified(file_path):
    """
    Get the last modification date of a file from git history.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str or None: Last modification date in ISO format or None if not found
    """
    try:
        output = subprocess.check_output(["git", "log", "-1", "--format=%ci", file_path], encoding="utf-8")
        return output.strip()
    except subprocess.CalledProcessError:
        return None

def update_file(file_path):
    """
    Update the lastUpdated field in the frontmatter of an MDX file.
    
    Args:
        file_path (str): Path to the MDX file
        
    Returns:
        bool: True if file was updated, False otherwise
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    last_mod = get_last_modified(file_path)
    if not last_mod:
        print(f"Could not determine last modified time for {file_path}")
        return False

    updated = False

    # Update or insert lastUpdated field.
    # Check for placeholder pattern {LAST_UPDATED} as well as any existing timestamp
    placeholder_pattern = re.compile(r'(lastUpdated:\s*")(\{LAST_UPDATED\}|.*?)(")')
    if placeholder_pattern.search(content):
        new_content, count = placeholder_pattern.subn(r'\1' + last_mod + r'\3', content)
        if count > 0:
            content = new_content
            updated = True
    else:
        # If no lastUpdated field exists, add it
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                rest = parts[2]
                new_last_updated_line = f'lastUpdated: "{last_mod}"'
                frontmatter += f'\n{new_last_updated_line}\n'
                content = f'---{frontmatter}---{rest}'
                updated = True

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated lastUpdated metadata for {file_path}")
    return updated

# -------------------------------------------------------------------------------- #
# Main Execution
# -------------------------------------------------------------------------------- #
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
