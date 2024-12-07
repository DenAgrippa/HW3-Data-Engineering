import requests
from bs4 import BeautifulSoup
import json
import time
from html import unescape

# Получаем каталог жаропрочной спец. одежды с сайта Техноавиа, записываем в fireproof_wear_catalog.json
html_content = requests.get("https://ekaterinburg.technoavia.ru/katalog/spetsodezhda/fireproof_wear").text

soup = BeautifulSoup(html_content, "html.parser")
clothings = soup.find_all('li', {'class': 'model_li model_li_standart'})
items = []

for clothing in clothings:
    item = {}

    item['id'] = clothing['id']
    item['articul'] = float(clothing['articul'])
    item['price'] = float(clothing['price'])
    item['link'] = clothing.h3.a['href']
    item['name'] = unescape(clothing.h3.a.text).strip()
    item['short_name'] = clothing.img['alt']
    item['img_link'] = clothing.img['src']

    items.append(item)

with open("./results/5/fireproof_wear_catalog.json", "w", encoding="utf-8") as f:
    json.dump(items, f)



# Парсим страницы каждого предмета в каталоге, записываем в output.json
item_list = []
for page in items:
    html_content = requests.get(f"https://ekaterinburg.technoavia.ru/{page['link']}").text
    content = BeautifulSoup(html_content, "html.parser")

    item = {}
    item['articul'] = float(content.find('div', {'class': 'articul_art'}).text.strip())
    item['name'] = unescape(content.find('h1', {'class': 'modname'}).text.replace("\xa0", "").replace("Новинка", "").strip())
    item['price'] = int(unescape(content.find('div', {'class': 'model_price'}).text.replace("₽", "").replace("\xa0", "").strip()))
    item['props'] = []

    props = content.find_all('li', {'class': 'picto_li'})
    for prop in props:
        item['props'].append(prop.div['data-tipso-title'])

    if content.find('div', {'class': 'textopisanie_cont more'}) is not None:
        if content.find('div', {'class': 'textopisanie_cont more'}).h3 is not None:
            item['construct'] = content.find('div', {'class': 'textopisanie_cont more'}).h3.strong.text.strip()
    item_list.append(item)
    time.sleep(0.5)

with open("./results/5/output.json", "w", encoding="utf-8") as f:
    json.dump(item_list, f)



# Сортируем по цене, записываем результат в sorted_output.json
with open("./results/5/output.json", "r") as f:
    json_data = json.load(f)
    sorted_data = sorted(json_data, key= lambda x: x['price'])

with open("./results/5/sorted_output.json", "w", encoding="utf-8") as f:
    json.dump(sorted_data, f)



# Фильтруем данные, записываем результат в filtered_output.json
filtered_items = []

with open("./results/5/output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data:
        if "Имеет заключение Минпромторга России" in item['props']:
            filtered_items.append(item)

with open("./results/5/filtered_output.json", "w", encoding="utf-8") as f:
    json.dump(filtered_items, f)



# Рассчитываем статистические показатели для цены (записываем в price_stats.json) и считаем частоту меток по конструкции (записываем в construct_stats.json)
price_stats = {
    'sum': 0,
    'min': 'placeholder',
    'max': 0,
    'avg': 0,
}

construct_stats = {}

with open("./results/5/output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data:
        price = item['price']

        price_stats['sum'] += price
        if price_stats['min'] == 'placeholder' or price_stats['min'] > price:
            price_stats['min'] = price

        if price_stats['max'] < price:
            price_stats['max'] = price

        if "construct" in item:
            if item['construct'] not in construct_stats:
                construct_stats[item['construct']] = 1
            else:
                construct_stats[item['construct']] += 1

    price_stats['avg'] = price_stats['sum'] / len(json_data)
    
    print(price_stats)
    print(construct_stats)

with open("./results/5/price_stats.json", "w", encoding="utf-8") as f:
    json.dump(price_stats, f)

with open("./results/5/construct_stats.json", "w", encoding="utf-8") as f:
    json.dump(construct_stats, f)