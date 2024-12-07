import os
import json
from bs4 import BeautifulSoup



items = []

for filename in os.listdir('./data/3'):
    with open(f"./data/3/{filename}", "r", encoding="utf-8") as f:
        xml_content = f.read()

        star = BeautifulSoup(xml_content, "xml").star
        item = {}

        for el in star:
            if el.name is None: continue
            item[el.name] = el.get_text().strip()
        item['radius'] = int(item['radius'])

        items.append(item)

with open("./results/3/output.json", "w", encoding="utf-8") as f:
    json.dump(items, f)



# Сортируем по радиусу, записываем результат в sorted_output.json
with open("./results/3/output.json", "r") as f:
    json_data = json.load(f)
    sorted_data = sorted(json_data, key= lambda x: x['radius'])

with open("./results/3/sorted_output.json", "w", encoding="utf-8") as f:
    json.dump(sorted_data, f)



# Фильтруем данные, записываем результат в filtered_output.json
filtered_items = []

with open("./results/3/output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data:
        if "constalation" in item and item['constalation'] == "Стрелец":
            filtered_items.append(item)

with open("./results/3/filtered_output.json", "w", encoding="utf-8") as f:
    json.dump(filtered_items, f)



# Рассчитываем статистические показатели для радиуса (записываем в radius_stats.json) и считаем частоту меток по созвездию (записываем в matrix_stats.json)
radius_stats = {
    'sum': 0,
    'min': 'placeholder',
    'max': 0,
    'avg': 0,
}

constellation_stats = {}

with open("./results/3/output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data:
        radius = item['radius']

        radius_stats['sum'] += radius
        if radius_stats['min'] == 'placeholder' or radius_stats['min'] > radius:
            radius_stats['min'] = radius

        if radius_stats['max'] < radius:
            radius_stats['max'] = radius

        if item['constellation'] not in constellation_stats:
            constellation_stats[item['constellation']] = 1
        else:
            constellation_stats[item['constellation']] += 1

    radius_stats['avg'] = radius_stats['sum'] / len(json_data)
    
    print(radius_stats)
    print(constellation_stats)

with open("./results/3/radius_stats.json", "w", encoding="utf-8") as f:
    json.dump(radius_stats, f)

with open("./results/3/constellation_stats.json", "w", encoding="utf-8") as f:
    json.dump(constellation_stats, f)