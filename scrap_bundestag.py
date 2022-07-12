import time

import requests
from bs4 import BeautifulSoup
import json

# Скрипт для парсинга сайта www.bundestag.de
# Задача
# Нужно взять всех членов парламента и составить Json файл с их именами и ссылками на аккаунты

# Приготовление списка ссылок с сайта

# persons_url_list = []
#
# for i in range(0, 750, 20):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
#
#     q = requests.get(url)
#     result = q.content
#
#     soup = BeautifulSoup(result, 'lxml')
#
#     persons = soup.find_all(class_='bt-open-in-overlay')
#
#     for person in persons:
#         person_page_url = person.get('href')
#
#         persons_url_list.append(person_page_url)
#
# with open('persons_url_list.txt', 'a') as file:
#     for line in persons_url_list:
#         file.write(f'{line}\n')

data_dict = []
count = 0

with open('persons_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]
    for line in lines:

        q = requests.get(line)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')

        t = soup.find(class_='bt-biografie-name')
        t2 = t.find('h3')
        person = t2.text
        person_name_company = person.strip().split(',')
        person_name = person_name_company[0].strip()
        person_company = person_name_company[1].strip()

        social_networks = soup.find_all(class_='bt-link-extern')

        social_networks_urls = []
        for item in social_networks:
            social_networks_urls.append(item.get('href'))

        data = {
            'person_name': person_name,
            'person_company': person_company,
            'social_networks_url': social_networks_urls
        }

        count += 1
        print(f'{count}: {line} is done')

        data_dict.append(data)

        time.sleep(2)

with open('result.json', 'a') as json_file:
    json.dump(data_dict, json_file, indent=4)