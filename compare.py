# -*- coding: utf8 -*-

# compare.py
# Dani Suarez - suarezdanieltomas@gmail.com

from fileparse import parse_csv
import ezgmail


def compare_prices(filename):
    with open(filename, 'rt') as f:
        data = parse_csv(f, types=[str, float, float])
        today_prices = data[-1]
        yesterday_prices = data[-2]
        headers = [header for header in data[0] if header != 'fecha']
        alert = ''
        for header in headers:
            if today_prices[header] < yesterday_prices[header]:
                alert += (f'The product {header} is '
                          f'{yesterday_prices[header] - today_prices[header]} '
                          f'USD cheaper today! (US ${today_prices[header]})\n')
    return alert


def alert_if_cheaper(alert):
    if alert:
        ezgmail.init()
        ezgmail.send('danisuarez94@gmail.com',#,cristelyacovone96@gmail.com',
                     'Alert from analizando el mercado',
                     alert)
