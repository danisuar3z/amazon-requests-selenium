# -*- coding: utf8 -*-

# main.py
# Dani Suarez - suarezdanieltomas@gmail.com

import sys
from datetime import date
import csv
import req_scraper as req
from selen_scraper import open_firefox, get_price, close_firefox
from compare import compare_prices, alert_if_cheaper


def read_urls(filename):
    '''
    pre: urls is text file with comma-separated-values
    and has an url header
    pos: returns a list with the urls in that column
    '''
    with open(filename, 'rt') as f:
        rows = csv.reader(f)
        headers = next(rows)
        urls = []
        for row in rows:
            url = dict(zip(headers, row))
            urls.append(url['url'])
    return urls


def scrape_with_req(urls):
    prices = [req.scrape(url) for url in urls]
    return prices


def scrape_with_selen(urls):
    print('Opening Firefox...')
    driver = open_firefox()
    prices = []
    for i, url in enumerate(urls, 1):
        if i == 1:
            print('This one\'s tricky, let me change the zip code...')
            price = get_price(url, driver, change_zip_code=True)
        else:
            print('Loading...')
            price = get_price(url, driver)
        prices.append(price)
    print('Closing Firefox...')
    close_firefox(driver)
    return prices


def export(prices, filename):
    today = date.today().isoformat()
    out = f'{today},{",".join(prices)}\n'
    with open(filename, 'at') as f:
        f.write(out)


def main(argv):
    print('Hey there! let\'s anaLIZAR EL MERCADO RUFIAN')
    urls = read_urls(argv[1])
    print('Fetching data with requests module...')
    prices = scrape_with_req(urls)

    failed_indexes = []
    for i, price in enumerate(prices):
        if 'ERROR' in price:
            failed_indexes.append(i)

    if failed_indexes:
        print('Trying now with selenium module, please lend me your browser')
        failed_urls = [urls[i] for i in failed_indexes]
        prices_fixed = scrape_with_selen(failed_urls)
    # Change the errors with the new scraped prices
    for i, failed_index in enumerate(failed_indexes):
        prices[failed_index] = prices_fixed[i]

    export(prices, argv[2])

    alert = compare_prices(argv[2])
    if alert:
        alert_if_cheaper(alert)


if __name__ == '__main__':
    main(sys.argv)
