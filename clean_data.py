import os
import re
import json
from glob import glob
from multiprocessing import Pool

# Function to remove unnecessary sections
def remove_unnecessary_sections(text):
    """Remove legal notices, navigation menus, and other redundant sections."""
    patterns = [
        r'Legal Notice.*?(?=\n\n|\Z)',           # Legal disclaimers
        r'Navigation.*?(?=\n\n|\Z)',            # Navigation menus
        r'Table of Contents.*?(?=\n\n|\Z)',     # TOCs
        r'Copyright ©.*?(?=\n\n|\Z)',           # Copyright footers
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()

# Extract title
def extract_title(text):
    """Extract a concise title from the document."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "Untitled"
    # Pattern to capture product name, version, and title
    match = re.search(r'Home Products (.+?)( \d+\.\d+| \d{4}\.Q\d)? (.+?)( Open|$)', lines[0])
    if match:
        product, version, title = match.groups()[0], match.groups()[1], match.groups()[2]
        return f"{product}{version or ''} {title}".strip()
    return lines[0].split(" Open")[0].strip()

# Extract version
def extract_version(text):
    """Extract version numbers like 'OpenShift version 4.12' or 'RHEL 8.5'."""
    version_pattern = r'(\d+\.\d+|\d{4}\.Q\d|Version \d+\.\d+)'
    # Check the first few lines for version information
    for line in text.split('\n')[:5]:
        match = re.search(version_pattern, line)
        if match:
            return match.group(1)
    # Fallback: search the entire text
    match = re.search(version_pattern, text)
    return match.group(1) if match else None

# Extract meaningful sections
def extract_sections(text):
    """Split text into sections based on numbered or appendix headings."""
    section_pattern = r'^(?:\d+(?:\.\d+)*\s+.*|Appendix [A-Z]\.\s+.*)$'
    sections = []
    current_section = None
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if re.match(section_pattern, line):
            if current_section:
                sections.append(current_section)
            current_section = {'heading': line, 'content': ''}
        elif current_section and line:
            current_section['content'] += line + '\n'
    
    if current_section and current_section['content'].strip():
        sections.append(current_section)
    
    # If no sections found, treat the entire text as a single section
    if not sections and text.strip():
        sections.append({'heading': 'Main Content', 'content': text.strip()})
    
    return sections

# Extract CLI commands
def extract_commands(text):
    """Extract lines that look like CLI commands."""
    command_pattern = r'^\s*[\$>] .+|^.*\b(kubectl|oc|rpm|artemis|mvn)\b.*$'
    commands = []
    for line in text.split('\n'):
        if re.match(command_pattern, line.strip()):
            commands.append(line.strip())
    return commands

# Process a single document
def process_document(file_path):
    """Process one document and return structured data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Clean the text
        cleaned_text = remove_unnecessary_sections(text)
        
        # Extract components
        title = extract_title(cleaned_text)
        version = extract_version(cleaned_text)
        sections = extract_sections(cleaned_text)
        commands = extract_commands(cleaned_text)
        
        # Structure the data
        document_data = {
            'title': title,
            'version': version,
            'sections': [{'heading': s['heading'], 'content': s['content'].strip()} 
                         for s in sections],
            'commands': commands
        }
        return document_data
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Main processing function with parallelization
def main():
    input_dir = 'datasets/redhat'  # Directory containing .txt files
    output_file = 'pre_processed_data.jsonl'
    
    # Get list of text files
    txt_files = glob(os.path.join(input_dir, '*.txt'))
    print(f"Found {len(txt_files)} documents to process.")
    
    # Use multiprocessing to process files in parallel
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_document, txt_files)
    
    # Write results to JSONL
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for result in results:
            if result:  # Skip failed documents
                json.dump(result, out_f)
                out_f.write('\n')
    
    print(f"Processing complete. Output saved to {output_file}")

if __name__ == '__main__':
    main()
