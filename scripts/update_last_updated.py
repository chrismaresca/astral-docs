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
        # Convert to simple YYYY-MM-DD format
        date_str = output.strip()
        if date_str:
            # Extract just the date portion (YYYY-MM-DD) from the git timestamp
            date_only = date_str.split()[0]
            return date_only
        return None
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
    new_last_updated_line = f'lastUpdated: "{last_mod}"'

    # First, look for the existing frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            rest = parts[2]
            
            # Check if lastUpdated already exists in any form
            last_updated_exists = re.search(r'lastUpdated:', frontmatter)
            
            # Handle existing lastUpdated field
            if last_updated_exists:
                # Replace the entire line containing lastUpdated
                lines = frontmatter.split('\n')
                new_lines = []
                for line in lines:
                    if line.strip().startswith('lastUpdated:'):
                        new_lines.append(new_last_updated_line)
                    else:
                        new_lines.append(line)
                new_frontmatter = '\n'.join(new_lines)
                content = f'---{new_frontmatter}---{rest}'
                updated = True
            else:
                # Add new lastUpdated field
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
