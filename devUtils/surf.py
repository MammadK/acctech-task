import os
import re
import json

# List of files to be excluded
excluded_files = ["index.html"]

def process_html_file(file_path):
    translation_data = {}
    non_matching_text = []  # List to store text that does not match the conditions

    with open(file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

        # allElements = re.findall(r'>([^<]+)<', html_content)
        allElements = re.findall(r'<[^/>]*>([^<]+)</[^>]*>', html_content)
        excludedElements = re.findall(r'</[^>]*>([^<]+)<[^>]*>', html_content)

        # Use list comprehensions to filter allElements
        text_elements = [element for element in allElements if element not in excludedElements]

        


        for text in text_elements:
            # Remove leading and trailing whitespace and newline characters
            finalText = text.strip()

            # Remove consecutive spaces and newlines
            finalText = ' '.join(finalText.split())

            # Check conditions for text filtering

            excluded_chars = r'[{}()@/$<>#]|^\d+[\W\d]*$|^[^\w\s&]+$|\d{2}:\d{2}|^\+|^\w$'


            english_chars = r'[^A-Za-z0-9_]'

            if (
                finalText and
                not re.search(excluded_chars, finalText) and
                not finalText.isspace()
            ):
                # Convert original text to uppercase and create object key
                object_key = finalText.upper().replace(' ', '_')
                object_key = re.sub(english_chars, '', object_key)

                # Add underscore at the beginning if object_key starts with a digit
                if object_key[0].isdigit():
                    object_key = '_' + object_key

                # Remove consecutive underscores (no repetitive _)
                object_key = re.sub(r'(_)\1+', r'\1', object_key)

                if len(object_key) > 25:
                    object_key = object_key[:25]

                # Replace the text within HTML tags with the 'translate' attribute
                html_content = html_content.replace(f'>{text}<', f' translate="X.{object_key}"><')

                # Store the data in the dictionary
                translation_data[object_key] = finalText
            else:
                if finalText.strip():
                    # If text does not match conditions, add it to the non-matching text list
                    non_matching_text.append(text)

        # Save the modified HTML content back to the file
        with open(file_path, 'w', encoding='utf-8') as modified_html_file:
            modified_html_file.write(html_content)

    return translation_data, non_matching_text

def save_non_matching_text(non_matching_text):
    with open('./devUtils/excluded-texts111.txt', 'w', encoding='utf-8') as txt_file:
        for text in non_matching_text:
            txt_file.write(text + '\n' + '*****\n')


def traverse_and_process(base_dir):
    data = {}  # Stores the translation data
    processed_files = 0  # Counter for processed files
    non_matching_text = []  # List to store text that does not match the conditions

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html') and 'assets' not in root and file not in excluded_files:
                file_path = os.path.join(root, file)
                translation_data, non_matching = process_html_file(file_path)
                data.update(translation_data)
                non_matching_text.extend(non_matching)
                processed_files += 1

    # Print the number of processed files
    print(f"Processed {processed_files} files.")

    # Save the translation data to extracted-texts.json
    with open('./devUtils/extracted-texts111.json', 'w', encoding='utf-8') as js_file:
        js_file.write(json.dumps(data, ensure_ascii=False, indent=2))

    # Save non-matching text to a .txt file
    save_non_matching_text(non_matching_text)

if __name__ == "__main__":
    base_directory = './src'
    traverse_and_process(base_directory)