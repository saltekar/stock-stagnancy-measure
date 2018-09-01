import ssl
import urllib

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup

from stock_stagnancy_research import StockStagnancyResearch
from stock_general_research import StockGeneralResearcher
import stagnancy_graph

app = Flask(__name__)

VALUE_MONTHS_ERROR = 'Invalid entry for months, did not receive integer. Received value: {}.'
RANGE_MONTHS_ERROR = 'Invalid entry for months. Integer must be in range from 1 to 240. Received value: {}.'
VALUE_TICKER_ERROR = 'Invalid entry for ticker symbol. Received value: {}'
API_OVERLOAD = 'Servers overloaded. Please wait a few moments and try again.'
ERROR404 = 'Page not found.'
ERROR500 = 'Server Error.'


@app.route('/resume')
@app.route('/')
def resume():
    return render_template('resume.html')


@app.route('/stagnancy-researcher', methods=['GET', 'POST'])
def stock_researcher():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol'].upper()

        if is_valid(ticker_symbol) is False:
            return redirect(url_for('.error', error=VALUE_TICKER_ERROR.format(ticker_symbol)))

        try:
            past_months = int(request.form['past_months'])
        except ValueError:
            return redirect(url_for('.error', error=VALUE_MONTHS_ERROR.format(request.form['past_months'])))

        if past_months > 240 or past_months == 0:
            return redirect(url_for('.error', error=RANGE_MONTHS_ERROR.format(past_months)))

        return redirect('/stagnancy-researcher/result?ticker_symbol=%s&past_months=%i' % (ticker_symbol, past_months))

    return render_template('stagnancy_researcher.html')


@app.route('/stagnancy-researcher/result')
def result():
    ticker_symbol = request.args['ticker_symbol'].upper()
    past_months = int(request.args['past_months'])

    try:
        stock_stagnancy = StockStagnancyResearch(ticker_symbol, past_months)
    except KeyError:
        return redirect(url_for('.error', error=API_OVERLOAD))

    stock_general = StockGeneralResearcher(ticker_symbol)

    divs = get_graphs(ticker_symbol, past_months, stock_stagnancy)
    div_timeseries = divs[0]
    div_custom_graph = divs[1]

    return render_template('result.html', ticker_symbol=stock_stagnancy.ticker_symbol, past_months=stock_stagnancy.months,
                           stagnancy_index=stock_stagnancy.get_stagnant_index(), avg_volume=stock_stagnancy.get_avg_volume(),
                           company_name=stock_general.get_data('companyName'), market_cap=stock_general.get_data('marketcap'),
                           beta=stock_general.get_data('beta'), week52_high=stock_general.get_data('week52high'),
                           week52_low=stock_general.get_data('week52low'), short_interest=stock_general.get_data('shortInterest'),
                           dividend_yield=stock_general.get_data('dividendYield'), ex_dividend_date=stock_general.get_data('exDividendDate'),
                           latest_eps=stock_general.get_data('latestEPS'), shares_outstanding=stock_general.get_data('sharesOutstanding'),
                           ebitda=stock_general.get_data('EBITDA'), revenue=stock_general.get_data('revenue'),
                           gross_profit=stock_general.get_data('grossProfit'), cash=stock_general.get_data('cash'),
                           debt=stock_general.get_data('debt'),  short_ratio=stock_general.get_data('shortRatio'),
                           price=stock_general.get_price(), pe_ratio=stock_general.get_data('peRatio'),
                           day50_moving_avg=stock_general.get_data('day50MovingAvg'), day200_moving_avg=stock_general.get_data('day200MovingAvg'),
                           revenue_per_share=stock_general.get_data('revenuePerShare'), return_assets=stock_general.get_data('returnOnAssets'),
                           dividend_rate=stock_general.get_data('dividendRate'), graph_timeseries=Markup(div_timeseries),
                           graph_custom=Markup(div_custom_graph))


@app.route('/stagnancy-researcher/about')
def about():
    return render_template('about.html')


@app.route('/stagnancy-researcher/error')
def error():
    msg = request.args['error']

    return render_template('error.html', error=msg)


@app.errorhandler(404)
def page_not_found():
    return redirect(url_for('.error', error=ERROR404))


@app.errorhandler(500)
def server_error():
    return redirect(url_for('.error', error=ERROR500))


def get_graphs(ticker_symbol, past_months, stock_stagnancy):
    """
    Returns list of string divs for graphs.
    """

    high_data_all = stock_stagnancy.get_all_data('2. high')
    low_data_all = stock_stagnancy.get_all_data('3. low')

    high_data = stock_stagnancy.get_data(past_months, '2. high')
    low_data = stock_stagnancy.get_data(past_months, '3. low')

    dates = stock_stagnancy.get_all_dates()

    return [stagnancy_graph.get_graph(ticker_symbol, high_data_all, low_data_all, dates),
            stagnancy_graph.get_custom_graph(ticker_symbol, past_months, high_data, low_data, dates)]


def is_valid(ticker_symbol):
    """
    Returns true if ticker_symbol is valid.
    """
    url = 'https://api.iextrading.com/1.0/stock/%s/quote' % ticker_symbol

    try:
        context = ssl._create_unverified_context()
        urllib.request.urlopen(url, context=context)
    except:
        return False

    return True

