import json
from translate import Translator
from tqdm import tqdm
import requests


# Define your proxy information
proxy_url = "127.0.0.1:10809"  # Replace with your proxy URL and port
proxy_auth = requests.auth.HTTPProxyAuth("your-username", "your-password")  # Replace with your proxy username and password

# Set up a proxy session
proxy_session = requests.Session()
proxy_session.proxies = {"http": proxy_url, "https": proxy_url}
# proxy_session.auth = proxy_auth


def translate_to_persian(text):
    try:
        translator = Translator(to_lang="fa", from_lang="en", session=proxy_session)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return None


def main():
    # Load the JSON data from the 'en2.json' file
    with open('./devUtils/remained.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create dictionaries to store the translated values and errors
    translated_data = {}
    translation_errors = {}

    # Create a tqdm progress bar to track the translation progress
    progress_bar = tqdm(total=len(data), position=0, leave=True, desc="Translating")

    # Translate the values from English to Persian and print them
    for key, value in data.items():
        translated_value = translate_to_persian(value)
        if translated_value is not None:
            translated_data[key] = translated_value
        else:
            translation_errors[key] = value
        progress_bar.update(1)
        progress_bar.set_postfix(Translated=translated_value)

    # Close the progress bar
    progress_bar.close()

    # Save the translated data to a new file
    with open('translated_fa.json', 'w', encoding='utf-8') as output_file:
        json.dump(translated_data, output_file, ensure_ascii=False, indent=4)

    # Save the translation errors to a separate file
    with open('translation-errors.json', 'w', encoding='utf-8') as errors_file:
        json.dump(translation_errors, errors_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
