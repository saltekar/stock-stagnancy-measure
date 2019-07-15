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

        # Need new api to get this info
        url_price = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=price' % ticker_symbol
        url_stats = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=defaultKeyStatistics' % ticker_symbol
        url_finance = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=financialData' % ticker_symbol
        url_summary = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=summaryDetail' % ticker_symbol

        # Pulls various data form pull requests
        context = ssl._create_unverified_context()
        price_json = urllib.request.urlopen(url_price, context=context)
        stats_json = urllib.request.urlopen(url_stats, context=context)
        finance_json = urllib.request.urlopen(url_finance, context=context)
        summary_json = urllib.request.urlopen(url_summary, context=context)

        # Loads data in json format
        self.price_data = json.load(price_json)
        self.stats_data = json.load(stats_json)
        self.finance_data = json.load(finance_json)
        self.summary_data = json.load(summary_json)

        # Empty dict - going to store all data in one common place
        self.data = {}

        self.set_price_data()
        self.set_stats_data()
        self.set_finance_data()
        self.set_summary_data()

    def set_price_data(self):
        """
        Sets all the price data in a dictionary.
        :return: None
        """
        price = self.price_data["quoteSummary"]["result"][0]["price"]

        self.data["companyName"] = price["longName"]
        self.data["marketcap"] = price["marketCap"]["fmt"]

    def set_stats_data(self):
        """
        Sets all the stats data in dict.
        :return: None
        """
        stats = self.stats_data["quoteSummary"]["result"][0]["defaultKeyStatistics"]

        self.data["beta"] = stats["beta"]["fmt"]
        self.data["week52change"] = stats["52WeekChange"]["fmt"]
        self.data["latestEPS"] = stats["trailingEps"]["fmt"]
        self.data["sharesOutstanding"] = stats["sharesOutstanding"]["fmt"]
        self.data["floatShares"] = stats["floatShares"]["fmt"]
        self.data["shortRatio"] = stats["shortRatio"]["fmt"]

    def set_finance_data(self):
        """
        Sets all the finance data in dict.
        :return: None
        """
        finance = self.finance_data["quoteSummary"]["result"][0]["financialData"]

        self.data["EBITDA"] = finance["ebitda"]["fmt"]
        self.data["revenue"] = finance["totalRevenue"]["fmt"]
        self.data["grossProfit"] = finance["grossProfits"]["fmt"]
        self.data["cash"] = finance["freeCashflow"]["fmt"]
        self.data["debt"] = finance["totalDebt"]["fmt"]
        self.data["revenuePerShare"] = finance["revenuePerShare"]["fmt"]
        self.data["returnOnAssets"] = finance["returnOnAssets"]["fmt"]

    def set_summary_data(self):
        """
        Sets all the summary data in dict.
        :return: None
        """
        summary = self.summary_data["quoteSummary"]["result"][0]["summaryDetail"]

        self.data["week52high"] = summary["fiftyTwoWeekHigh"]["fmt"]
        self.data["week52low"] = summary["fiftyTwoWeekLow"]["fmt"]
        self.data["dividendYield"] = summary["dividendYield"]["fmt"]
        self.data["exDividendDate"] = summary["exDividendDate"]["fmt"]
        self.data["peRatio"] = summary["trailingPE"]["fmt"]
        self.data["day50MovingAvg"] = summary["fiftyDayAverage"]["fmt"]
        self.data["day200MovingAvg"] = summary["twoHundredDayAverage"]["fmt"]
        self.data["dividendRate"] = summary["dividendRate"]["fmt"]

    def get_data(self, data_type):
        """
        Gets data from the dictionary for specific key
        :param data_type: type of data ex. market cap
        """
        return self.data[data_type]
