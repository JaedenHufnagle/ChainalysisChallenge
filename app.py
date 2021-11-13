from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import os
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from requests.sessions import session

app = Flask(__name__)
application = app
bootstrap = Bootstrap(app)

#App configs
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#Links for exchanges
elink1 = 'https://exchange.blockchain.com/trade/ETH-USD'
blink1 = 'https://exchange.blockchain.com/trade/-USD?utm_source=CMC&utm_medium=CMC&utm_campaign=CMCsponsorship&tid=102fe8e781cb17f6f4f047a6f0603a'
elink2 = 'https://messari.io/'
blink2 = 'https://messari.io/'

#Api 1 call to coinmarket to get prices of first exchange
def apicall():

    #Api call
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'symbol':'BTC,ETH',
    'convert':'USD',
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'b32dd36b-1492-4f89-8b24-9da3863bf8f0',
    }

    session = Session()
    session.headers.update(headers)

    #Breaking apart the data into prices and selling points
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        i = 0
        dd = data['data']
        ETH = dd['ETH']
        quoteE = ETH['quote']
        USDE = quoteE['USD']
        priceE = USDE['price']
        BTC = dd['BTC']
        quote = BTC['quote']
        USD = quote['USD']
        price = USD['price']
        sell = price + (price * (USD['percent_change_24h']/100))
        selle = priceE + (priceE * (USDE['percent_change_24h']/100))
        return [round(price,2),round(priceE,2),round(sell,2),round(selle,2)]

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

#Api call for Messari
def apicall2():

    url = "https://data.messari.io/api/v1/assets/btc/metrics"
    url2= "https://data.messari.io/api/v1/assets/eth/metrics"
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        response2 = session.get(url2)
        data2 = json.loads(response2.text)
        dd2 = data2['data']
        marketdata2 = dd2['market_data']
        price2 = marketdata2['price_usd']
        och2 = marketdata2['ohlcv_last_1_hour']
        close2 = och2['close']
        dd = data['data']
        marketdata = dd['market_data']
        price = marketdata['price_usd']
        och = marketdata['ohlcv_last_1_hour']
        close = och['close']
        return [round(price,2),round(price2,2),round(close,2),round(close2,2)]
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

@app.route('/', methods = ['GET','POST'])
def home():
    price = apicall()
    price2 = apicall2()
    esurl=''
    eburl=''
    bsurl=''
    bburl=''
    apicall2()
    if price[0]<=price2[0]:
        bburl = blink1
    else:
        bburl = blink2
    if price[2]>=price2[2]:
        bsurl = blink1
    else:
        bsurl = blink2
    if price[1]<=price2[1]:
        eburl = elink1
    else:
        eburl = elink2
    if price[3]>=price2[3]:
        esurl = elink1
    else:
        esurl = elink2

    return render_template('Home.html',bprice=price[0], bprice2=price2[0], eprice=price[1], eprice2=price2[1],bsell=price[2],bsell2=price2[2],
    esell=price[3],esell2=price2[3],bblink = bburl, eblink = eburl, eslink = esurl, bslink = bsurl)