import os
from bs4 import BeautifulSoup
import re
import json

# Base directory to start the search
base_directory = './src'  # Replace with your base directory

# Function to process inner text and create the JavaScript object
def process_html_file(file_path):
    with open(file_path, 'rb') as file:
        html_content = file.read()
        try:
            # Attempt to decode the file using UTF-8
            html_content = html_content.decode('utf-8')
        except UnicodeDecodeError:
            # Handle encoding issues
            print(f"Error reading file {file_path}: Encoding issue")

    soup = BeautifulSoup(html_content, 'html.parser')

    translations = {}

    for tag in soup.find_all():
        if tag.string is not None:
            originalText = tag.string.strip()  # Remove trailing spaces and replace newline with space
            originalText = originalText.replace('\n', ' ')

            # Check if originalText meets the specified conditions
            if not (originalText.isdigit() or
                    re.match(r'^\d+\s\d+$', originalText) or
                    re.match(r'^\d+,\d+$', originalText) or
                    '{' in originalText or
                    '(' in originalText or
                    ')' in originalText or
                    '%' in originalText or
                    '/' in originalText or
                    '\\' in originalText or
                    'pm' in originalText.lower() or
                    'am' in originalText.lower() or
                    '@' in originalText or
                    '.com' in originalText or
                    '$' in originalText):
                # Convert originalText to uppercase, replace space with '_', remove ' and limit to 25 characters
                objectKey = '_'.join(originalText.upper().split()).replace("'", '')[:25]
                # Ensure objectKey only contains English characters, '_', and digits
                objectKey = re.sub(r'[^A-Z0-9_]', '', objectKey)
                # If objectKey is not empty, add it to the translations with a comment
                if objectKey:
                    comment = f"// {os.path.relpath(file_path, base_directory)}"
                    translations[objectKey] = (originalText, comment)

    return translations

# Function to traverse subfolders and process HTML files
def traverse_folders_and_process(base_folder):
    translations = {}

    for root, dirs, files in os.walk(base_folder):
        if 'assets' in dirs:
            dirs.remove('assets')  # Exclude the 'assets' directory

        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                translations.update(process_html_file(file_path))

    return translations

# Run the function to traverse subfolders and process HTML files
translations = traverse_folders_and_process(base_directory)

# Save the translations to a JavaScript object
with open('EN.js', 'w', encoding='utf-8') as js_file:
    js_file.write('var translations = {\n')
    for key, value in translations.items():
        js_file.write(f'{value[1]}\n')
        js_file.write(f'"{key}": "{value[0]}",\n')
    js_file.write('};')

print("Processing completed.")
