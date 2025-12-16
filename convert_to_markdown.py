#!/usr/bin/env python3
"""
Convert Minna no Nihongo text files to markdown format for GitHub Pages.
"""

import os
import re
from pathlib import Path


def convert_file_to_markdown(input_path, output_path):
    """Convert a single text file to markdown format."""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Start building markdown content
    md_content = []
    
    # Parse header information
    title = ""
    isbn = ""
    version = ""
    author = ""
    
    vocabulary_started = False
    header_written = False
    
    for line in lines:
        line = line.rstrip()
        
        # Parse header comments
        if line.startswith('# Minna no Nihongo'):
            title = line[2:].strip()
            continue
        elif line.startswith('# ISBN'):
            isbn = line[2:].strip()
            continue
        elif line.startswith('# Version'):
            version = line[2:].strip()
            continue
        elif line.startswith('# Paul Denisowski'):
            author = line[2:].strip()
            continue
        elif line == '#end':
            break
        elif line.startswith('#'):
            continue
            
        # Skip empty lines before vocabulary starts
        if not line and not vocabulary_started:
            continue
            
        # Now we're in vocabulary section - write header first
        if line and not vocabulary_started:
            vocabulary_started = True
            # Write header
            md_content.append(f"# {title}\n\n")
            md_content.append("## Grammar\n\n")
            md_content.append("## Vocabulary\n\n")
            md_content.append("| Kanji/Kana | Reading | Meaning |\n")
            md_content.append("|------------|---------|----------|\n")
        
        if vocabulary_started and line:
            # Parse vocabulary line: word [reading] /meaning/
            match = re.match(r'^(.+?)\s+\[(.+?)\]\s+/(.+)/$', line)
            if match:
                word = match.group(1).strip()
                reading = match.group(2).strip()
                meaning = match.group(3).strip()
                md_content.append(f"| {word} | {reading} | {meaning} |\n")
    
    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    
    print(f"Converted: {input_path.name} -> {output_path.name}")


def main():
    """Main conversion function."""
    base_dir = Path(__file__).parent
    
    # Convert mnn1_all files
    mnn1_dir = base_dir / 'mnn1_all'
    mnn1_output_dir = base_dir / 'mnn1_all'
    
    if mnn1_dir.exists():
        for txt_file in sorted(mnn1_dir.glob('*.txt')):
            # Extract lesson number from filename: Minna_no_nihongo_1.01.txt -> 01
            match = re.search(r'_(\d)\.(\d+)\.txt$', txt_file.name)
            if match:
                book_num = match.group(1)
                lesson_num = match.group(2)
                # Create new filename: minna_no_nihongo_sho_1_x_01.md
                new_name = f"minna_no_nihongo_sho_{book_num}_x_{lesson_num}.md"
                md_file = mnn1_output_dir / new_name
                convert_file_to_markdown(txt_file, md_file)
    
    # Convert mnn2_all files
    mnn2_dir = base_dir / 'mnn2_all'
    mnn2_output_dir = base_dir / 'mnn2_all'
    
    if mnn2_dir.exists():
        for txt_file in sorted(mnn2_dir.glob('*.txt')):
            # Extract lesson number from filename: Minna_no_nihongo_2.26.txt -> 26
            match = re.search(r'_(\d)\.(\d+)\.txt$', txt_file.name)
            if match:
                book_num = match.group(1)
                lesson_num = match.group(2)
                # Create new filename: minna_no_nihongo_sho_2_x_26.md
                new_name = f"minna_no_nihongo_sho_{book_num}_x_{lesson_num}.md"
                md_file = mnn2_output_dir / new_name
                convert_file_to_markdown(txt_file, md_file)
    
    print("\nConversion complete!")


if __name__ == '__main__':
    main()
