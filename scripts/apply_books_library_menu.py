import os, glob

with open('scripts/nav_menu_template.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Extract books_library_html
marker = "books_library_html = '''"
start = code.find(marker)
end = code.find("'''", start + len(marker))
books_library_html = code[start + len(marker):end]

# Target all active html pages in root
html_files = glob.glob('*.html')
print(f"Found {len(html_files)} HTML pages in root to inspect.")

updated_count = 0
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if left-strip-bar exists
    if 'left-strip-bar' not in content:
        continue

    # If books-library group is already present, skip
    if 'data-group="books-library"' in content:
        print(f"Skipping {hf}, already has books-library menu.")
        continue

    # Insert right after the 7 Ashram Books group: data-group="books"
    # Find the closing </div> of strip-sub-menu or strip-group for data-group="books"
    pattern_marker = '<div class="strip-group" data-group="books">'
    pos = content.find(pattern_marker)
    if pos != -1:
        # Find next strip-group
        next_pos = content.find('<div class="strip-group"', pos + len(pattern_marker))
        if next_pos != -1:
            new_content = content[:next_pos] + books_library_html + '\n      ' + content[next_pos:]
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1
            print(f"Updated {hf} with Books Library menu group!")
        else:
            print(f"Could not find next strip-group in {hf}")
    else:
        # If no data-group="books", try before data-group="school" or </nav>
        school_pos = content.find('<div class="strip-group" data-group="school">')
        if school_pos != -1:
            new_content = content[:school_pos] + books_library_html + '\n      ' + content[school_pos:]
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1
            print(f"Updated {hf} before school group!")

print(f"\nTotal HTML files updated with Books Library menu: {updated_count}")
