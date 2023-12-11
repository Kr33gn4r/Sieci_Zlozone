import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
import random
import json

def get_wikipedia_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text_content = ' '.join([p.get_text() for p in paragraphs])
    return text_content

def get_wikipedia_categories(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories_section = soup.find('div', {'id': 'catlinks'})
    categories = [a.get_text() for a in categories_section.find_all('a', href=True) if
                  a.get('href').startswith('/wiki/Category:')]
    return categories

def get_wikipedia_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Znajdź odnośniki tylko w treści artykułu (pomiń odnośniki w nagłówkach, stopkach itp.)
    article_div = soup.find('div', {'id': 'mw-content-text'})
    links = [a.get('href') for a in article_div.find_all('a', href=True) if
             a.get('href') and a.get('href').startswith('/wiki/') and ':' not in a.get('href')]

    return links

def explore_recursive_wikipedia_links(start_urls, depth, num_links=10, data=None):
    if data is None:
        data = []

    for start_url in start_urls:
        explore_recursive_wikipedia_links_helper(start_url, depth, num_links, data)

    return data

def explore_recursive_wikipedia_links_helper(url, depth, num_links, data):
    if depth <= 0:
        return

    for _ in range(num_links):
        links = get_wikipedia_links(url)
        if not links:
            break

        link = random.choice(links)
        new_url = f'https://en.wikipedia.org{link.replace(" ", "_")}'  # Zamień spacje na podkreślenie
        text_content = get_wikipedia_content(new_url)
        tokenized_text = word_tokenize(text_content)  # Tokenizacja tekstu przy użyciu NLTK
        categories = get_wikipedia_categories(new_url)
        label = categories[0] if categories else None
        print(f"URL: {new_url}, Label: {label}")

        # Zapisz dane
        data.append({'url': new_url, 'text': tokenized_text, 'label': label})

        # Rekurencyjnie pobierz nowe linki
        explore_recursive_wikipedia_links_helper(new_url, depth - 1, num_links, data)

# Przykład użycia
start_urls = ['https://en.wikipedia.org/wiki/Machine_learning']
depth = 3
num_links = 10

# Eksploracja i zapis danych
data = explore_recursive_wikipedia_links(start_urls, depth, num_links)

# Zapisz dane do pliku JSON
with open('wikipedia_data_recursive.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)