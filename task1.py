import os
import json
from bs4 import BeautifulSoup



items = []

for filename in os.listdir('./data/1'):
    with open(f"./data/1/{filename}", "r", encoding="utf-8") as f:
        html_content = f.read()
        item = {}

        soup = BeautifulSoup(html_content, "html.parser")

        item['name'] = soup.find("h1", {'class': 'title'}).text.split(":")[1].strip()
        item['id'] = soup.find("h1", {'class': 'title'})['id']
        item['availability'] = soup.find("span").text.split("Наличие:")[1].strip()
        address_price_container = soup.find("p", {'class': "address-price"}).text.split("Цена:")
        item['address'] = address_price_container[0].split(":")[1].strip()
        item['price'] = int(address_price_container[1].strip().strip(" руб"))
        item['color'] = soup.find("span", {'class': 'color'}).text.split(':')[1].strip()
        item['quantity'] = int(soup.find("span", {'class': 'quantity'}).text.split(':')[1].strip().strip(" шт"))
        item['dimensions'] = soup.find("span", text= lambda text: text.strip().startswith("Размеры")).text.split(":")[1].strip()
        item['rating'] = float(soup.find("span", text= lambda text: text.strip().startswith("Рейтинг")).text.split(":")[1].strip())
        item['views'] = int(soup.find("span", text= lambda text: text.strip().startswith("Просмотры")).text.split(":")[1].strip())
        item['img_link'] = soup.img['src']

        items.append(item)


with open("./results/1/output.json", "w", encoding="windows-1251") as f:
    json.dump(items, f)



# Сортируем по рейтингу, записываем результат в sorted_output.json
with open("./results/1/output.json", "r") as f:
    json_data = json.load(f)
    sorted_data = sorted(json_data, key= lambda x: x['rating'], reverse=True)

with open("./results/1/sorted_output.json", "w", encoding="utf-8") as f:
    json.dump(sorted_data, f)



# Фильтруем данные, записываем результат в filtered_output.json
filtered_items = []

with open("./results/1/output.json", "r") as f:
    json_data = json.load(f)

    for item in json_data:
        if item['color'] != "Синий":
            filtered_items.append(item)

with open("./results/1/filtered_output.json", "w", encoding="utf-8") as f:
    json.dump(filtered_items, f)



# Рассчитываем статистические показатели для цены (записываем в price_stats.json) и считаем частоту меток по цвету (записываем в color_stats.json)
price_stats = {
    'sum': 0,
    'min': 'placeholder',
    'max': 0,
    'avg': 0,
}

color_stats = {}

with open("./results/1/output.json", "r") as f:
    json_data = json.load(f)

    for item in json_data:
        price = item['price']

        price_stats['sum'] += price
        if price_stats['min'] == 'placeholder' or price_stats['min'] > price:
            price_stats['min'] = price

        if price_stats['max'] < price:
            price_stats['max'] = price

        if item['color'] not in color_stats:
            color_stats[item['color']] = 1
        else:
            color_stats[item['color']] += 1

    price_stats['avg'] = price_stats['sum'] / len(json_data)
    
    print(price_stats)
    print(color_stats)

with open("./results/1/price_stats.json", "w") as f:
    json.dump(price_stats, f)

with open("./results/1/color_stats.json", "w") as f:
    json.dump(color_stats, f)
