# -------------------------------------------------------------------------------- #
# Documentation File Renamer
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
import os
import re
import shutil

# -------------------------------------------------------------------------------- #
# File Renaming Functions
# -------------------------------------------------------------------------------- #

# Define the order of files in each directory
directory_file_order = {
    "01-getting-started": [
        "installation",
        "quick-start",
        "available-models"
    ],
    "02-authentication": [
        "overview",
        "authentication-methods",
        "using-templates",
        "template-builder-beta"
    ],
    "03-providers": [
        "openai",
        "anthropic", 
        "gemini",
        "aws-sagemaker",
        "groq",
        "azure-openai",
        "aws-bedrock",
        "google-vertex-ai",
        "hugging-face",
        "openrouter",
        "ollama"
    ],
    "04-guides": [
        "quick-start",
        "tool-calling",
        "using-mcp",
        "running-evaluations",
        "fallback-models"
    ],
    "05-errors": [
        "index"
    ]
}

def rename_files():
    """Rename .mdx files to include sequential numbering."""
    base_dir = "docs/v1"
    
    for dir_name, file_order in directory_file_order.items():
        dir_path = os.path.join(base_dir, dir_name)
        
        # If the directory exists
        if os.path.exists(dir_path):
            print(f"Processing directory: {dir_path}")
            
            # Process files in the specified order
            for i, base_name in enumerate(file_order, 1):
                old_path = os.path.join(dir_path, f"{base_name}.mdx")
                new_path = os.path.join(dir_path, f"{i:02d}-{base_name}.mdx")
                
                # If the file exists with the old name
                if os.path.exists(old_path):
                    print(f"  Renaming: {old_path} -> {new_path}")
                    shutil.move(old_path, new_path)
                else:
                    print(f"  File not found: {old_path}")
        else:
            print(f"Directory not found: {dir_path}")

# -------------------------------------------------------------------------------- #
# Main Execution
# -------------------------------------------------------------------------------- #

if __name__ == "__main__":
    rename_files() 