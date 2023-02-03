import requests
import json
from config import keys


class APIException(Exception):
    pass


class CoinConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')
    
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
    
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data_js = json.loads(data.content)
        
        if quote_ticker == 'RUB':
            total_base = round(1 / data_js['Valute'][base_ticker]['Value'] * amount, 3)
        elif base_ticker == 'RUB':
            total_base = round(data_js['Valute'][quote_ticker]['Value'] * amount, 3)
        else:
            total_base = round(data_js['Valute'][quote_ticker]['Value'] / data_js['Valute'][base_ticker]['Value'] * amount, 3)
        
        return total_base