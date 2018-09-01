import requests
from bdateutil import isbday, relativedelta
import holidays
from datetime import date


class StockStagnancyResearch:
    """
    Researches stock based on certain amount of past months. Finds stagnancy.
    """

    def __init__(self, ticker_symbol, months=0):
        """
        Constructor for stock stagnancy research class.
        :param months: number of months back user wants to research
        """

        self.months = months
        self.ticker_symbol = ticker_symbol
        self.stock_dates = self.get_stock_json()
        self.past_data_close = self.get_data(months, "4. close")  # Gets closing data for past months given by user
        self.past_data_vol = self.get_data(months, "5. volume")  # Gets volume data for past months given by user

    def get_stock_json(self):
        """
        Returns dictionary of stock dates and information.
        """
        # API info
        url = "https://www.alphavantage.co/query"
        func = "TIME_SERIES_DAILY"
        api_key = "SF9TWTH9FPEYUV8S"  # Go to https://www.alphavantage.co/ to get your own API key
        output_size = "full"

        data = {"function": func,
                "symbol": self.ticker_symbol,
                "outputsize": output_size,
                "apikey": api_key}

        stock_info = requests.get(url, params=data)
        stock_data = stock_info.json()

        return stock_data["Time Series (Daily)"]

    def get_all_data(self, data_type):
        """
        Returns a list of all the data.
        :param data_type: type of data
        """
        prices = []

        for day in self.stock_dates:
            prices.append(float(self.stock_dates[day][data_type]))

        return prices

    def get_data(self, months, data_type):
        """
        Returns a list of the data.
        :param months: number of months back user wants to research
        :param data_type: type of data (ex. closing values)
        """

        start_date = self.get_start_date(months)
        prices = []

        for day in self.stock_dates:
            prices.append(float(self.stock_dates[day][data_type]))
            if day == start_date:
                break

        return prices

    def get_start_date(self, past_months):
        """
        Returns the date user wants to start collecting information.
        :param past_months: number of months back user wants to research
        """

        current_date = list(self.stock_dates.keys())[0]  # Gets most current day of the stock market

        year = int(current_date[:4])
        month = int(current_date[5:7])
        day = int(current_date[8:10])

        begin_date = date(year, month, day)-relativedelta(months=past_months)

        year = begin_date.year
        month = begin_date.month
        day = begin_date.day

        # Changes single digit to double.
        if len(str(month)) is 1:
            month = "0" + str(month)

        if len(str(day)) is 1:
            day = "0" + str(day)

        # Date changes format.
        start_date = str(year) + "-" + str(month) + "-" + str(day)

        # Checks to make sure start date is a business day, if not moves to next business day.
        if not isbday(start_date, holidays=holidays.US()):
            start_date += relativedelta(bdays=+1, holidays=holidays.US())

        return str(start_date)[:10]

    def get_all_dates(self):
        """
        Returns a list of all dates stock has been public.
        """
        dates = []

        dict_data = self.stock_dates

        for date_ in dict_data.keys():
            dates.append(date_)

        return dates

    def get_stagnant_index(self):
        """
        Returns stagnant index. Formula finds sum of difference of mean and values, then divides everything by mean.
        """
        mean = self.get_avg(self.past_data_close)

        total = 0
        for val in self.past_data_close:
            total += abs(mean - val)

        total = total / len(self.past_data_close)

        return round((total / mean) * 100, 5)

    def get_avg_volume(self):
        """
        Returns daily average volume of the stock.
        """
        avg_vol = self.get_avg(self.past_data_vol)

        if not isinstance(avg_vol, str):
            avg_vol = self.int_format(float(avg_vol))

        return avg_vol

    @staticmethod
    def get_avg(data):
        """
        Returns average of all elements in a list.
        """
        total = 0

        for val in data:
            total += val

        return total / len(data)

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

    def __str__(self):
        """
        Returns string of research for stock.
        """
        return self.ticker_symbol + " (Last " + str(self.months) + " months)" + ": \nStangancy Index: " + \
               str(self.get_stagnant_index()) + "\nAvg Daily Vol: " + str(self.get_avg_volume())
