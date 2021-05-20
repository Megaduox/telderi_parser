import lxml
import requests

from bs4 import BeautifulSoup
from queue import Queue

BASE_URL = 'telderi.ru'
DOMAIN = f'https://www.{BASE_URL}/'
URLS_QUEUE = Queue()
URLS_BASE = set()
FILTER = {'/search/', '/sort_by/', '/show/', '/uploads/', '/viewBid'}


def crawler():

    while True:

        if URLS_QUEUE.qsize() == 0 or URLS_QUEUE.qsize() > 50:
            break

        url = URLS_QUEUE.get()
        URLS_BASE.add(url)

        response = requests.get(url)
        response.raise_for_status()
        print('Scanning url ', url, 'Status code is ', response.status_code)

        soup = BeautifulSoup(response.content, 'lxml')

        for link in soup.find_all('a'):
            link = link.get('href')
            if DOMAIN not in str(link):
                continue
            if any(part in link for part in FILTER):
                continue

            print(link)

            URLS_QUEUE.put(link)


if __name__ == '__main__':
    URLS_QUEUE.put(DOMAIN)
    try:
        crawler()
    except requests.HTTPError as error:
        print('Ошибка при запросе ', error)