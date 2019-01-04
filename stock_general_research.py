import json
import ssl
import urllib
from urllib.request import urlopen


class StockGeneralResearcher:
    """
    Gets general information of stock from API.
    """

    def __init__(self, ticker_symbol):
        """
        Constructor for stock general researcher class.
        """
        self.ticker_symbol = ticker_symbol

        url_general = 'https://api.iextrading.com/1.0/stock/%s/stats' % ticker_symbol
        url_price = 'https://api.iextrading.com/1.0/stock/%s/price' % ticker_symbol
        url_quote = 'https://api.iextrading.com/1.0/stock/%s/quote' % ticker_symbol

        context = ssl._create_unverified_context()
        general_request = urllib.request.urlopen(url_general, context=context)
        price_request = urllib.request.urlopen(url_price, context=context)
        quote_request = urllib.request.urlopen(url_quote, context=context)

        self.price = json.load(price_request)
        self.general = json.load(general_request)
        self.quote = json.load(quote_request)

    def get_data(self, data_type):
        """
        Returns specific data based on type needed.
        :param data_type: type of data ex. market cap
        """
        data = self.general
        data.update(self.quote)

        list_data_nums = ['revenue', 'marketcap', 'grossProfit', 'EBITDA', 'cash', 'debt', 'sharesOutstanding',
                          'shortInterest']

        for type_num in list_data_nums:
            if not isinstance(data[type_num], str):
                data[type_num] = self.int_format(float(data[type_num]))

        if isinstance(data[data_type], float):
            data[data_type] = round(data[data_type], 2)

        return data[data_type]

    def get_company_name(self):
        """
        Returns company name.
        """

        return self.general['companyName']

    def get_price(self):
        """
        Returns current price of stock.
        """

        return self.price

    @staticmethod
    def int_format(num):
        """
        Returns shortened number by adding word-number suffix.
        :param num: number to shorten
        """
        value = ''

        if num > 1000000000000:
            num /= 1000000000000
            value = 'T'
        elif num > 1000000000:
            num /= 1000000000
            value = 'B'
        elif num > 1000000:
            num /= 1000000
            value = 'M'

        return str(round(num, 2)) + value
