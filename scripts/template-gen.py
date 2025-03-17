# -------------------------------------------------------------------------------- #
# Documentation Template Generator
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
import os
import re

# -------------------------------------------------------------------------------- #
# Template Generation Functions
# -------------------------------------------------------------------------------- #

def create_template_content(title):
    """Create template content for documentation files."""
    return f"""---
title: {title}
description: {title} documentation for ASTRAL
lastUpdated: "{{LAST_UPDATED}}"
---

# {title}

Content coming soon...
"""

def normalize_title(filename):
    """Convert filename to title format."""
    # Remove file extension
    name = os.path.splitext(filename)[0]
    
    # Replace hyphens with spaces
    name = name.replace('-', ' ')
    
    # Special handling for specific prefixes
    if name == "index":
        return "Overview"
    
    # Handle special cases
    special_cases = {
        "aws bedrock": "AWS Bedrock",
        "aws sagemaker": "AWS Sagemaker",
        "openai": "OpenAI",
        "azure openai": "Azure OpenAI",
        "hugging face": "Hugging Face",
        "google vertex ai": "Google Vertex AI",
        "openrouter": "OpenRouter",
        "ollama": "Ollama",
        "mcp": "MCP"
    }
    
    # Check for special cases
    for case, replacement in special_cases.items():
        if name.lower() == case:
            return replacement
    
    # Title case for everything else
    return ' '.join(word.capitalize() for word in name.split())

def apply_templates():
    """Apply templates to all .mdx files in the docs/v1 directory."""
    for root, _, files in os.walk("docs/v1"):
        for file in files:
            if file.endswith(".mdx"):
                filepath = os.path.join(root, file)
                
                # For existing files, check if they need the lastUpdated field
                if os.path.getsize(filepath) > 0:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    # If lastUpdated is missing, add it
                    if "lastUpdated: " not in content:
                        # Extract title or use filename
                        title_match = re.search(r'title: "(.*?)"', content)
                        if title_match:
                            title = title_match.group(1)
                        else:
                            title = normalize_title(file)
                        
                        # Create new content
                        new_content = create_template_content(title)
                        with open(filepath, 'w') as f:
                            f.write(new_content)
                        print(f"Updated template for: {filepath}")
                    continue
                
                # Create new files
                title = normalize_title(file)
                content = create_template_content(title)
                
                with open(filepath, 'w') as f:
                    f.write(content)
                
                print(f"Created template for: {filepath}")

# -------------------------------------------------------------------------------- #
# Main Execution
# -------------------------------------------------------------------------------- #

if __name__ == "__main__":
    apply_templates() 