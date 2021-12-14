import json
import requests
from bs4 import BeautifulSoup

data_ozon_items = []

def ozon_scr(count):
    for k in range(1,count+1):
        url = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=/category/termopasta-30799/?from_global=true&page={k}&text=%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D0%BF%D0%B0%D1%81%D1%82%D0%B0&page_changed=true'

        headers = {
            'content-type': 'application/json; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        req = requests.get(url, headers=headers)

        with open('ozon_page.json', 'w', encoding='utf-8') as file:
            json.dump(req.json(),file, ensure_ascii=False, indent=4)
        with open('ozon_page.json', encoding='utf-8') as file:
            file_content = file.read()
        site_json = json.loads(file_content)
        for i in site_json['trackingPayloads'].values():
            z = json.loads(i)
            try:
                data_ozon_items.append({
                    'name': z['title'],
                    'rang':z['index'],
                    'id': z['id'],
                    'old_price': z['price'],
                    'price': z['finalPrice'],
                    'rating': z['rating'],
                    'feedback': z['countItems'],
                    'brand': z['brand'],
                    'url': f'ozon.ru{z["link"]}'
                })
            except Exception as ex:
                pass
    data_info = [dict(t) for t in {tuple(d.items()) for d in data_ozon_items}]
    with open('data_Ozon.json', 'w', encoding='utf-8') as file:
        json.dump(data_info, file, ensure_ascii=False, indent=4)

def ozon_stock(count):
    list_Items = []
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    req1 = requests.get(
        'https://www.ozon.ru/category/termopasta-30799/?from_global=true&text=%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D0%BF%D0%B0%D1%81%D1%82%D0%B0',
        headers=headers)
    with open('ozon_page.html', 'w', encoding='utf-8') as file:
        file.write(req1.text)
    with open('ozon_page.html', 'r', encoding='utf-8') as file:
        file_content = file.read()
    soup = BeautifulSoup(file_content, 'html.parser')
    count_id = soup.find('div', id='state-searchResultsV2-311201-default-1')
    find_count = count_id.get('data-state')
    site_json = json.loads(find_count)
    with open('ozon_stock.json', 'w', encoding='utf-8') as file:
        json.dump(site_json, file)
    with open('ozon_stock.json', 'r', encoding='utf-8') as file:
        file_contetn2 = file.read()
    stock_count = json.loads(file_contetn2)
    for i in stock_count['items']:
        list_Items.append({
            'id': int(i['multiButton']['ozonButton']['addToCartButtonWithQuantity']['action'].get('id')),
            'stock': i['multiButton']['ozonButton']['addToCartButtonWithQuantity'].get('maxItems'),
            'img': i['tileImage']['images'][0]
        })
    for z in range(2,count+1):
        print(z)
        req = requests.get(f'https://www.ozon.ru/category/termopasta-30799/?from_global=true&page={z}&text=%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D0%BF%D0%B0%D1%81%D1%82%D0%B0', headers=headers)
        with open('ozon_page.html', 'w', encoding='utf-8') as file:
            file.write(req.text)
        with open('ozon_page.html', 'r', encoding='utf-8') as file:
            file_content = file.read()
        soup = BeautifulSoup(file_content, 'html.parser')
        count_id = soup.find('div', id ='state-searchResultsV2-311201-default-1')

        if count_id is None:
            with open('stock_Ozon.json', 'w', encoding='utf-8') as file:
                json.dump(list_Items, file, indent=4, ensure_ascii=False)
            return z-1
            break

        else:
            find_count = count_id.get('data-state')
            site_json = json.loads(find_count)
            with open('ozon_stock.json', 'w', encoding='utf-8') as file:
                json.dump(site_json,file)
            with open('ozon_stock.json', 'r', encoding='utf-8') as file:
                file_contetn2 = file.read()
            stock_count = json.loads(file_contetn2)
            for i in stock_count['items']:
                list_Items.append({
                    'id': int(i['multiButton']['ozonButton']['addToCartButtonWithQuantity']['action'].get('id')),
                    'stock':i['multiButton']['ozonButton']['addToCartButtonWithQuantity'].get('maxItems'),
                    'img': i['tileImage']['images'][0]
                })

def get_ozon():
    with open('data_Ozon.json', 'r', encoding='utf-8') as file:
        file_content = json.loads(file.read())
    with open('stock_Ozon.json', 'r') as file:
        file_content2 = json.loads(file.read())
    data_ozon = []
    for i in file_content2:
        for z in file_content:
            if i['id'] == z['id']:
                data_ozon.append(i|z)
    data_info = [dict(t) for t in {tuple(d.items()) for d in data_ozon}]
    data_ozon_end = sorted(data_info,key=lambda x:x['rang'])
    with open('ozon_data_end.json', 'w', encoding='utf-8') as file:
        json.dump(data_ozon_end,file,indent=4, ensure_ascii=False)

def main():
    count = ozon_stock(50)
    ozon_scr(count)
    get_ozon()

if __name__ == "__main__":
    main()