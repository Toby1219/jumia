import os
import csv
import json
import sqlite3
import time
from dataclasses import dataclass, asdict, astuple
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests_cache import CachedSession
import threading


session = CachedSession(
    cache_name='cache/jumia_cache',
)

main_path = 'data'
if not os.path.exists(main_path):
    os.mkdir(main_path)
else:
    pass


@dataclass
class Jumia:
    name: str = None
    price: float = None
    stars: float = None
    product_link: str = None


def get_response(link):
    try:
        respon = session.get(link)
        if respon.status_code == 200:
            print(respon.status_code)
            return respon
        else:
            print(respon.status_code)
            return 0
    except Exception as e:
        print(f'Error at get_response {e}')


def extract_text(soup, tags, sel, value):
    try:
        elem = soup.find(tags, sel).text.strip()
        return elem
    except:
        return f'No {value} data'


def pipline(value):
    chars = []
    for char in chars:
        if char in text:
            value = text.replace(char, '').strip()
            return value
        else:
            return text


def next_page(html):
    try:
        soup = BeautifulSoup(html.content, 'html5lib')
        next_url = soup.find('a', {"aria-label": "Next Page"})['href']
        abs_next_url = f'https://www.jumia.com.ng{next_url}'
        print(abs_next_url)
        if abs_next_url != 'https://www.jumia.com.ng/catalog/?q=itel&page=11#catalog-listing':
            return main(abs_next_url)
        else:
            raise Exception
    except Exception:
        print("No more pages")
        return None


def scraper(response):
    result = []
    result2 = []
    soup = BeautifulSoup(response.content, 'html5lib')
    article_product = soup.findAll('article', {'class': "prd _fb col c-prd"})
    for item in article_product:
        name = extract_text(item, 'h3', {'class': 'name'}, 'name')
        price = extract_text(item, 'div', {'class': 'prc'}, 'price')
        stars = extract_text(item, 'div', {'class': 'stars _s'}, 'rateing')
        urls = item.find('a', {'class': 'core'})['href']
        prod_url = f'https://www.jumia.com.ng{urls}'
        data = Jumia(
            name=name,
            price=price,
            stars=stars,
            product_link=prod_url
        )
        result.append(asdict(data))
        result2.append(astuple(data))
    return result, result2


def writer_to_json(data):
    path = 'data/jumia'
    if os.path.isfile(path):
        for datas in data:
            with open(f'{path}.json', 'r') as file:
                char = json.load(file)
            char.append(datas)
            with open(f'{path}.json', 'w', encoding='utf-8') as file:
                json.dump(char, file, indent=2, ensure_ascii=False)
    else:
        with open(f'{path}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


def writer_to_csv(data):
    paths = 'data/jumia'
    # file_exists = os.path.isfile(paths)
    field_name = list(data[0].keys())
    with open(f'{paths}.csv', 'a', newline='', encoding='utf-8') as csv_file:
        pen = csv.DictWriter(csv_file, fieldnames=field_name)
        csv_file.seek(0, 2)
        if csv_file.tell() == 0:
            pen.writeheader()
        # if not file_exists:
        #    pen.writeheader()
        pen.writerows(data)


def sql_writer(data):
    conn = sqlite3.connect('data/jumia.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS scraped_data (name TXT, price REAL, stars REAL, product_link TXT)")
    cur.executemany('INSERT INTO scraped_data VALUES (?, ?, ?, ?)', data)
    cur.execute('SELECT * FROM scraped_data')
    dat = cur.fetchall()
    for row in dat:
       print(row)


def main(link):
    response = get_response(link)
    result, result2 = scraper(response)
    writer_to_json(result)
    writer_to_csv(result)
    sql_writer(result2)
    next_page(response)
    # print('All Done....')


if __name__ == '__main__':
    start = time.perf_counter()
    url = 'https://www.jumia.com.ng/catalog/?q=itel'
    t1 = threading.Thread(target=main, args=[url])
    t1.start()
    t1.join()
    end = time.perf_counter()
    print()
    print(f'\nTime:{round(end - start, 2)} seconds')
