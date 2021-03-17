from iexfinance.stocks import Stock

# Enter your API Token here
token = ''

def fetch_current_price(stock_ticker):

    a = Stock(stock_ticker, token=token)
    return a.get_quote()['latestPrice'][0]

print(fetch_current_price('MSFT'))