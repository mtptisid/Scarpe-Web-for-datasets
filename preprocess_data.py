import json
import re

def escape_content(line):
    try:
        # First, check if it's already valid
        json.loads(line)
        return line  # If valid, return as is
    except json.JSONDecodeError:
        pass

    # Escape unescaped double quotes inside values
    def escape_match(match):
        content = match.group(1)
        escaped_content = content.replace('"', '\\"')  # Escape internal quotes
        return f'"content": "{escaped_content}"'
    
    pattern = r'("content":\s*")([^"]*)(")(?=\s*,\s*"[^"]+":|\s*})'
    escaped_line = re.sub(pattern, escape_match, line)

    try:
        json.loads(escaped_line)  # Validate again
        return escaped_line
    except json.JSONDecodeError as e:
        print(f"Final escape attempt failed: {e}")
        return None  # Mark it as a failure

# Now retry loading
with open("cleaned_redhat_docs_validated.jsonl", "r") as f:
    fixed_lines = []
    for i, line in enumerate(f, start=1):
        fixed_line = escape_content(line.strip())
        if fixed_line:
            fixed_lines.append(fixed_line)
        else:
            print(f"Skipping problematic line {i}")

# Save fixed JSON
with open("cleaned_redhat_docs_fixed.jsonl", "w") as f:
    for line in fixed_lines:
        f.write(line + "\n")
