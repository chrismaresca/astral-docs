#!/usr/bin/env python3
import os
import re
import sys

CODE_BLOCKS_DIR = os.path.join(os.getcwd(), "code-blocks")

# Updated pattern to use REPLACE_CODE_BLOCK: syntax instead of comments
PATTERN = re.compile(
    r'REPLACE_CODE_BLOCK:(CodeBlock|TerminalCommand)\s+filename:(\S+)(?:\s+language:(\S+))?(?:\s+package:(\S+))?\s*'
)


def infer_language(filename):
    ext = os.path.splitext(filename)[1].lower()
    return {
        '.sh': 'bash',
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript'
    }.get(ext, '')


def get_code_from_file(filename):
    file_path = os.path.join(CODE_BLOCKS_DIR, filename)
    if not os.path.exists(file_path):
        print(f"Warning: Code block file '{filename}' not found in {CODE_BLOCKS_DIR}")
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def replacement(match):
    component = match.group(1)
    filename = match.group(2)
    language = match.group(3) or infer_language(filename)
    package_manager = match.group(4)

    code_content = get_code_from_file(filename)
    if code_content is None:
        return match.group(0)
    code_content = code_content.replace("`", "\\`")
    if component == "CodeBlock":
        return f'<CodeBlock language="{language}" code={{`{code_content}`}} />'
    elif component == "TerminalCommand":
        if not package_manager:
            package_manager = "npm"
        return f'<TerminalCommand packageManager="{package_manager}" language="{language}" code={{`{code_content}`}} />'
    else:
        return match.group(0)


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, count = PATTERN.subn(replacement, content)
    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {count} component placeholder(s) in {file_path}")
        return True
    return False


def process_all_mdx(root_dir="docs"):
    updated_any = False
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".mdx"):
                full_path = os.path.join(subdir, file)
                if process_file(full_path):
                    updated_any = True
    if updated_any:
        print("One or more MDX files were updated with component replacements.")
    else:
        print("No MDX files required component updates.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file_path in sys.argv[1:]:
            process_file(file_path)
    else:
        process_all_mdx()
