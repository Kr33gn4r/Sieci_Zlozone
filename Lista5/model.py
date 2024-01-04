import json
import requests
from bs4 import BeautifulSoup
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split

def get_wikipedia_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text_content = ' '.join([p.get_text() for p in paragraphs])
    return text_content

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def process_text(tokens, url):
    print(f"Processing text for URL: {url}")
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    processed_words = [ps.stem(word.lower()) for word in tokens if word.isalnum() and word.lower() not in stop_words]
    return dict([(word, True) for word in processed_words])

def train_classifier(data):
    labeled_data = [(process_text(entry['text'], entry['url']), entry['label']) for entry in data if 'label' in entry]
    train_set, test_set = train_test_split(labeled_data, test_size=0.2)
    classifier = NaiveBayesClassifier.train(train_set)
    return classifier

def classify_new_text(classifier, text, url):
    processed_text = process_text(text, url)
    category = classifier.classify(processed_text)
    return category

# Wczytaj dane z pliku JSON
data = load_data_from_json('wikipedia_data_random_multiple.json')

# Trenuj klasyfikator
classifier = train_classifier(data)

# Przykład klasyfikacji nowego tekstu
url = 'https://en.wikipedia.org/wiki/Equivalence_principle'
new_text = get_wikipedia_content(url)
predicted_category = classify_new_text(classifier, new_text, url)
print(f"Predicted Category: {predicted_category}")