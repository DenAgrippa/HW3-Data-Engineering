import os
import json
from bs4 import BeautifulSoup



items = []

for filename in os.listdir('./data/4'):
    with open(f"./data/4/{filename}", "r", encoding="utf-8") as f:
        xml_content = f.read()
        soup = BeautifulSoup(xml_content, "xml")
        clothings = soup.find_all("clothing")

        for clothing in clothings:
            item = {}
            int_props = ["id", "reviews"]
            float_props = ["rating", "price"]
            boolean_props = ["new", "exclusive", "sporty"]

            for el in clothing:
                if el.name is None: 
                    continue
                elif el.name in int_props:
                    item[el.name] = int(el.get_text().strip())
                elif el.name in float_props:
                    item[el.name] = float(el.get_text().strip())
                elif el.name in boolean_props:
                    if el.get_text().strip().lower() == "yes" or el.get_text().strip() == "+":
                        item[el.name] = True
                    else:
                        item[el.name] = False
                else:
                    item[el.name] = el.get_text().strip()

            items.append(item)

with open("./results/4/output.json", "w", encoding="utf-8") as f:
    json.dump(items, f)



# Сортируем по рейтингу, записываем результат в sorted_output.json
with open("./results/4/output.json", "r") as f:
    json_data = json.load(f)
    sorted_data = sorted(json_data, key= lambda x: x['rating'], reverse=True)

with open("./results/4/sorted_output.json", "w", encoding="utf-8") as f:
    json.dump(sorted_data, f)



# Фильтруем данные, записываем результат в filtered_output.json
filtered_items = []

with open("./results/4/output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data:
        if "Addidas" in item['name']:
            filtered_items.append(item)

with open("./results/4/filtered_output.json", "w", encoding="utf-8") as f:
    json.dump(filtered_items, f)



# Рассчитываем статистические показатели для цены (записываем в price_stats.json) и считаем частоту меток по размеру (записываем в size_stats.json)
price_stats = {
    'sum': 0,
    'min': 'placeholder',
    'max': 0,
    'avg': 0,
}

size_stats = {}

with open("./results/4/output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data:
        price = item['price']

        price_stats['sum'] += price
        if price_stats['min'] == 'placeholder' or price_stats['min'] > price:
            price_stats['min'] = price

        if price_stats['max'] < price:
            price_stats['max'] = price

        if item['size'] not in size_stats:
            size_stats[item['size']] = 1
        else:
            size_stats[item['size']] += 1

    price_stats['avg'] = price_stats['sum'] / len(json_data)
    
    print(price_stats)
    print(size_stats)

with open("./results/4/price_stats.json", "w", encoding="utf-8") as f:
    json.dump(price_stats, f)

with open("./results/4/size_stats.json", "w", encoding="utf-8") as f:
    json.dump(size_stats, f)