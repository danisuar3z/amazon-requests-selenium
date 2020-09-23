# -*- coding: utf8 -*-

# req_scraper.py
# Dani Suarez - suarezdanieltomas@gmail.com

import requests
import bs4


def create_headers():
    headers = {
        'referer': 'https://www.amazon.com/',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/5'
        '37.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',

        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,imag'
        'e/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    return headers


def scrape(url):
    headers = create_headers()
    res = requests.get(url, headers=headers)
    if res.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in res.text:
            print('Blocked by amazon!')
        else:
            print('Error in request.')
        price = 'ERROR'
    else:
        soup = bs4.BeautifulSoup(res.text, features='html5lib')
        raw_price = soup.select('#priceblock_ourprice')
        price = raw_price[0].text.strip('US$\xa0')
    return price
