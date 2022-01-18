import requests
from bs4 import BeautifulSoup
import json
# from save_data import write_to_csv, write_to_json

MAIN_URL = 'https://vip.blokino.org/anime/'

def open_page(url):
    '''Открыает страницу по url и возвращает её содержимое'''
    response = requests.get(url)
    return response.text

def get_soup(page_content):
    '''Получате содержимое страницы в виде html, анализирует его и подгодавлевает к получению отдельных данных'''
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup

def get_products_cards(soup):
    '''Принимает код страницы и извлекает все карточки товаров'''
    listing = soup.find('div', class_='spisok')
    print(listing)
    cards = listing.find_all('div', class_='preview')
    return cards

def get_data_from_card(product_card):
    '''извлекает данные из конкретной карточки'''
    # {'image': '...', 'title':'...', 'description': '...', 'price': '...'}
    title = product_card.find('div', class_='perehod').find('a').text
    return {'title': title}

def write_to_json(data):
    with open('file_json.json', 'w+', encoding='utf8') as file:
        js_obj = json.dumps(data, ensure_ascii=False, indent=2)
        file.write(js_obj)

def main():
    products_cards = []
    current_page_url = f'{MAIN_URL}'
    page_content = open_page(current_page_url)
    soup = get_soup(page_content)
    cards = get_products_cards(soup)
    products_cards.extend(cards)
    data = []
    for card in products_cards:
        data.append(get_data_from_card(card))
    a = []
    for i in data:
        for s in i.values():
            a.append(s)
    print(a)
    return a



