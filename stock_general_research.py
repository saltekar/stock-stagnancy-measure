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

        self.set_defaults()
        self.set_price_data()
        self.set_stats_data()
        self.set_finance_data()
        self.set_summary_data()

    def set_defaults(self):
        """
        Sets all data in dict to N/A, in case some companies don't have these info.
        :return: None
        """
        self.data["marketcap"] = "N/A"
        self.data["beta"] = "N/A"
        self.data["week52change"] = "N/A"
        self.data["latestEPS"] = "N/A"
        self.data["sharesOutstanding"] = "N/A"
        self.data["floatShares"] = "N/A"
        self.data["shortRatio"] = "N/A"
        self.data["EBITDA"] = "N/A"
        self.data["revenue"] = "N/A"
        self.data["grossProfit"] = "N/A"
        self.data["cash"] = "N/A"
        self.data["debt"] = "N/A"
        self.data["revenuePerShare"] = "N/A"
        self.data["returnOnAssets"] = "N/A"
        self.data["week52high"] = "N/A"
        self.data["week52low"] = "N/A"
        self.data["dividendYield"] = "N/A"
        self.data["exDividendDate"] = "N/A"
        self.data["peRatio"] = "N/A"
        self.data["day50MovingAvg"] = "N/A"
        self.data["day200MovingAvg"] = "N/A"
        self.data["dividendRate"] = "N/A"

    def set_price_data(self):
        """
        Sets all the price data in a dictionary.
        :return: None
        """
        price = self.price_data["quoteSummary"]["result"][0]["price"]

        self.data["companyName"] = price["longName"]

        if "fmt" in price["marketCap"].keys():
            self.data["marketcap"] = price["marketCap"]["fmt"]

    def set_stats_data(self):
        """
        Sets all the stats data in dict.
        :return: None
        """
        stats = self.stats_data["quoteSummary"]["result"][0]["defaultKeyStatistics"]

        if "fmt" in stats["beta"].keys():
            self.data["beta"] = stats["beta"]["fmt"]
        if "fmt" in stats["52WeekChange"].keys():
            self.data["week52change"] = stats["52WeekChange"]["fmt"]
        if "fmt" in stats["trailingEps"].keys():
            self.data["latestEPS"] = stats["trailingEps"]["fmt"]
        if "fmt" in stats["sharesOutstanding"].keys():
            self.data["sharesOutstanding"] = stats["sharesOutstanding"]["fmt"]
        if "fmt" in stats["floatShares"].keys():
            self.data["floatShares"] = stats["floatShares"]["fmt"]
        if "fmt" in stats["shortRatio"].keys():
            self.data["shortRatio"] = stats["shortRatio"]["fmt"]

    def set_finance_data(self):
        """
        Sets all the finance data in dict.
        :return: None
        """
        finance = self.finance_data["quoteSummary"]["result"][0]["financialData"]

        if "fmt" in finance["ebitda"].keys():
            self.data["EBITDA"] = finance["ebitda"]["fmt"]
        if "fmt" in finance["totalRevenue"].keys():
            self.data["revenue"] = finance["totalRevenue"]["fmt"]
        if "fmt" in finance["grossProfits"].keys():
            self.data["grossProfit"] = finance["grossProfits"]["fmt"]
        if "fmt" in finance["freeCashflow"].keys():
            self.data["cash"] = finance["freeCashflow"]["fmt"]
        if "fmt" in finance["totalDebt"].keys():
            self.data["debt"] = finance["totalDebt"]["fmt"]
        if "fmt" in finance["revenuePerShare"].keys():
            self.data["revenuePerShare"] = finance["revenuePerShare"]["fmt"]
        if "fmt" in finance["returnOnAssets"].keys():
            self.data["returnOnAssets"] = finance["returnOnAssets"]["fmt"]

    def set_summary_data(self):
        """
        Sets all the summary data in dict.
        :return: None
        """
        summary = self.summary_data["quoteSummary"]["result"][0]["summaryDetail"]

        if "fmt" in summary["fiftyTwoWeekHigh"].keys():
            self.data["week52high"] = summary["fiftyTwoWeekHigh"]["fmt"]
        if "fmt" in summary["fiftyTwoWeekLow"].keys():
            self.data["week52low"] = summary["fiftyTwoWeekLow"]["fmt"]
        if "fmt" in summary["dividendYield"].keys():
            self.data["dividendYield"] = summary["dividendYield"]["fmt"]
        if "fmt" in summary["exDividendDate"].keys():
            self.data["exDividendDate"] = summary["exDividendDate"]["fmt"]
        if "fmt" in summary["trailingPE"].keys():
            self.data["peRatio"] = summary["trailingPE"]["fmt"]
        if "fmt" in summary["fiftyDayAverage"].keys():
            self.data["day50MovingAvg"] = summary["fiftyDayAverage"]["fmt"]
        if "fmt" in summary["twoHundredDayAverage"].keys():
            self.data["day200MovingAvg"] = summary["twoHundredDayAverage"]["fmt"]
        if "fmt" in summary["dividendRate"].keys():
            self.data["dividendRate"] = summary["dividendRate"]["fmt"]

    def get_data(self, data_type):
        """
        Gets data from the dictionary for specific key
        :param data_type: type of data ex. market cap
        """
        return self.data[data_type]
