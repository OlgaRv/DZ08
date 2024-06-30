from flask import Flask, render_template, request
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    quote = None
    author = None
    quote_text = get_random_quote()
    if quote_text:
        quote = quote_text.get('content', 'No quote available')
        author = quote_text.get('author', 'Unknown')
        translate_quote = translate_text(quote)
        translate_author = translate_text(author)
    else:
        translate_quote = "Ошибка при получении цитаты"
        translate_author = "Неизвестный"

    return render_template('index.html', quote=translate_quote, author=translate_author)


def get_random_quote():
    url = 'https://api.quotable.io/random'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None


def translate_text(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='ru').translate(text)
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return text  # Return the original text if translation fails


if __name__ == '__main__':
    app.run(debug=True)
