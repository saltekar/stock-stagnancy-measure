import plotly.graph_objs as go
import plotly
from stock_general_research import StockGeneralResearcher


def get_graph(ticker_symbol, high_data, low_data, dates):
    """
    Makes graph for multiple months. Returns a string div.
    :param dates: dates data goes back to
    :param low_data: data for stock lows
    :param high_data: data for stock highs
    """
    #stock_general = StockGeneralResearcher(ticker_symbol)

    trace_high = go.Scatter(
        x=dates,
        y=high_data,
        name="%s High" % ticker_symbol,
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_low = go.Scatter(
        x=dates,
        y=low_data,
        name="%s Low" % ticker_symbol,
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_high, trace_low]

    layout = dict(
        #title='%s Stock Time Series Graph' % stock_general.get_company_name()'
        title='%s Stock Time Series Graph' % ticker_symbol,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=3,
                         label='3m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=9,
                         label='9m',
                         step='month',
                         stepmode='backward'),
                    dict(count=24,
                         label='24m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            title='Time',
            type='date'
        ),
        yaxis=dict(
            title='Stock Price',
            type='linear'
        )
    )

    fig = dict(data=data, layout=layout)

    div = plotly.offline.plot(fig, output_type='div')

    return div


def get_custom_graph(ticker_symbol, past_months, high_data, low_data, dates):
    """
    Makes graph for given past months of a stock. Returns a string div.
    :param dates: dates data goes back to
    :param low_data: data for stock lows
    :param high_data: data for stock highs
    :param past_months: Number of months graph goes back.
    """
    #stock_general = StockGeneralResearcher(ticker_symbol)

    trace_high = go.Scatter(
        x=dates,
        y=high_data,
        name="%s High" % ticker_symbol,
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_low = go.Scatter(
        x=dates,
        y=low_data,
        name="%s Low" % ticker_symbol,
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_high, trace_low]

    layout = dict(
        title='%s Stock Graph For Past %i Months' % (ticker_symbol, past_months),
        #title='Stock Graph For Past %i Months' % (past_months),
        xaxis=dict(
            rangeslider=dict(
                visible=False
            ),
            title='Time',
            type='date'
        ),
        yaxis=dict(
            title='Stock Price',
            type='linear'
        )
    )

    fig = dict(data=data, layout=layout)

    div = plotly.offline.plot(fig, output_type='div')

    return div
