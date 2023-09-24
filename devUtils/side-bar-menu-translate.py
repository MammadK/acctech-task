# 'src/app/_metronic/layout/components/sidebar/sidebar-menu/sidebar-menu.component.html'

from bs4 import BeautifulSoup
import json

# Read the HTML file
with open('src/app/_metronic/layout/components/sidebar/sidebar-menu/sidebar-menu.component.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find elements with class="menu-title" and without a "translate" attribute
menu_title_elements = soup.find_all(class_='menu-title', attrs={'translate': False})

# Process the elements
translations = {}

for element in menu_title_elements:
    # Remove any trailing spaces and replace spaces between words with underscores
    text = '_'.join(element.get_text().strip().split())
    
    # Add the translate attribute
    element['translate'] = f"MENU.{text.upper()}"
    
    # Remove the innerText without affecting other attributes
    for content in element.contents:
        if content.name is None:
            content.extract()

    # Add translations to the dictionary
    translations[text.upper()] = "persian-translation"

# Save the modified HTML to a new file
with open('modified_html_file.html', 'w', encoding='utf-8') as modified_file:
    modified_file.write(soup.prettify())

# Save the translations to a JavaScript object
with open('translations.js', 'w', encoding='utf-8') as js_file:
    js_file.write(f'var translations = {json.dumps(translations, ensure_ascii=False, indent=2)};')

print("Processing completed.")
