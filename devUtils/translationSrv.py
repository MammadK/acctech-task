import json
from translate import Translator
from tqdm import tqdm

def translate_to_persian(text):
    translator = Translator(to_lang="fa", from_lang="en")
    translation = translator.translate(text)
    return translation

def main():
    # Load the JSON data from the 'en2.json' file
    with open('./devUtils/extracted-texts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create a dictionary to store the translated values
    translated_data = {}

    # Create a tqdm progress bar to track the translation progress
    progress_bar = tqdm(total=len(data), position=0, leave=True, desc="Translating")

    # Translate the values from English to Persian and print them
    for key, value in data.items():
        translated_value = translate_to_persian(value)
        translated_data[key] = translated_value
        progress_bar.update(1)
        progress_bar.set_postfix(Translated=translated_value)

    # Close the progress bar
    progress_bar.close()

    # Save the translated data to a new file
    with open('translated_fa.json', 'w', encoding='utf-8') as output_file:
        json.dump(translated_data, output_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
