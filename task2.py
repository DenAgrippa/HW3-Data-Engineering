import os
import json
import re
from bs4 import BeautifulSoup



items = []

for filename in os.listdir('./data/2'):
    with open(f"./data/2/{filename}", "r", encoding="utf-8") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        products = soup.find_all("div", {"class": "product-item"})

        for product in products:
            item = {}

            item['id'] = int(product.find("a", {"class": "add-to-favorite"})['data-id'])
            item['link'] = product.find_all("a")[1]['href']
            item['name'] = product.find("span").text.strip()
            item['price'] = float(product.find("price").text.replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(re.sub(r'[^\d]', '', product.find("strong").text))

            details = product.find_all("li")
            for detail in details:
                item[detail['type']] = detail.text.strip()
            
            items.append(item)

with open("./results/2/output.json", "w", encoding="utf-8") as f:
    json.dump(items, f)



# Сортируем по цене, записываем результат в sorted_output.json
with open("./results/2/output.json", "r") as f:
    json_data = json.load(f)
    sorted_data = sorted(json_data, key= lambda x: x['price'])

with open("./results/2/sorted_output.json", "w", encoding="utf-8") as f:
    json.dump(sorted_data, f)



# Фильтруем данные, записываем результат в filtered_output.json
filtered_items = []

with open("./results/2/output.json", "r") as f:
    json_data = json.load(f)

    for item in json_data:
        if "sim" in item and item['sim'] != "1 SIM":
            filtered_items.append(item)

with open("./results/2/filtered_output.json", "w", encoding="utf-8") as f:
    json.dump(filtered_items, f)



# Рассчитываем статистические показатели для ram (записываем в ram_stats.json) и считаем частоту меток по матрице (записываем в matrix_stats.json)
ram_stats = {
    'sum': 0,
    'min': 'placeholder',
    'max': 0,
    'avg': 0,
}

matrix_stats = {}

with open("./results/2/output.json", "r") as f:
    json_data = json.load(f)

    ram_length = 0
    for item in json_data:
        if "ram" in item:
            ram = int(item['ram'].replace("GB", "").strip())
            ram_length += 1
            ram_stats['sum'] += ram
            if ram_stats['min'] == 'placeholder' or ram_stats['min'] > ram:
                ram_stats['min'] = ram

            if ram_stats['max'] < ram:
                ram_stats['max'] = ram
        
        if "matrix" in item:
            if item['matrix'] not in matrix_stats:
                matrix_stats[item['matrix']] = 1
            else:
                matrix_stats[item['matrix']] += 1

    ram_stats['avg'] = ram_stats['sum'] / ram_length
    
    print(ram_stats)
    print(matrix_stats)

with open("./results/2/ram_stats.json", "w") as f:
    json.dump(ram_stats, f)

with open("./results/2/matrix_stats.json", "w") as f:
    json.dump(matrix_stats, f)