import streamlit as st

import pandas as pd
import numpy as np

import datetime as dt
import time
import boto3
import json
import requests
import base64

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import yfinance as yf
from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyCodes

from PIL import Image
global authValueFlag
authValueFlag = False
currentFunction = ""

def auth(authValueFlag):
    authValueFlag = False

img = Image.open('bitcoin.png')
st.set_page_config(page_title='Crypto Currency Forecast', page_icon=img, layout='wide')

col1, col2, col3, col4= st.beta_columns(4)

if authValueFlag == True:
    col4.button('Logout')

def main():
    menu = ['Login', 'Home', 'Architecture', "Crypto Currency Dashboard", 'Bitcoin Prediction', 'Sentiment Analysis']
    st.sidebar.title("** Menu **")
    choice = st.sidebar.selectbox("Select the page from dropdown to browse ", menu)

    # st.markdown('<style>body{background-color: #FFF2C2;}</style>', unsafe_allow_html=True)

    st.title("**_Crypto Currency Application_**")

    if choice == "Login":
        st.title("Login ")
        st.subheader("Enter your Username and Password:")
        usrname = st.text_input('Username')
        password = st.text_input('Password', type="password")
        email = st.text_input('Email')
        if st.button('Login'):
            f = open('AuthenticationValue.txt', 'a')
            f.truncate(0)
            current = open('Functionlocation.txt', 'a')
            current.truncate(0)
            try:
                aws_client = boto3.client('cognito-idp',
                                          region_name='us-east-2',
                                          # aws_access_key_id='AKIAWKCAZTNP6OC5P2VD',
                                          # aws_secret_access_key='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'
                                          )
                response = aws_client.admin_create_user(
                    UserPoolId='us-east-2_LUKFFoPeQ',
                    Username=usrname,
                    UserAttributes=[
                        {
                            'Name': "name",
                            'Value': usrname
                        },
                        {
                            'Name': "email",
                            'Value': email
                        }
                    ],
                    DesiredDeliveryMediums=['EMAIL']
                )
                st.info("user created")
                authValueFlag = True
                print(authValueFlag)
            except aws_client.exceptions.UsernameExistsException as e:
                st.info("Login successfully")

                authValueFlag = True
            f = open('AuthenticationValue.txt', 'a')
            f.truncate(0)
            f.write(str(authValueFlag))
            f.close()

    if choice == "Home":

        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                logout = col4.button('Logout')
                if logout:
                    authValueFlag = False
                    f = open('AuthenticationValue.txt', 'a')
                    f.truncate(0)
                    f.write(str(authValueFlag))
                    f.close()
                    st.info("You have been logged out!")
                    break
                img1 = Image.open('bitcoin2.png')
                st.image(img1)
                st.subheader('About:')
                st.write('A cryptocurrency, broadly defined, is currency that takes the form of tokens or “coins” and '
                         'exists on a distributed and decentralized ledger.Bitcoin continues to lead the pack of '
                         'cryptocurrencies in terms of market capitalization, user base, and popularity.')
                st.subheader('Content:')
                st.write("""- Crypto Currencies Market value between selected time frame 
                - An efficient Predictive model to forecast future trends for Bitcoin Market for the next 30 days 
                - Sentiment analysis on User reviews to detect possible correlations with the price of cryptocurrencies and digital tokens 
                - Technical indicators and Features such as Rate Of Change(ROC), Simple Moving Average, Exponential Moving Average """)
                st.subheader('Machine Learning Model:')
                st.write("""- We used LSTM(Long Short term Memory Model) frequently used for time series modeling. 
                - Trained the LSTM model on data scraped from Coin Index using features Open, High,Low and Close 
                - Trained the model on 3 years to predict the Bitcoin price for next 30 days 
                - Amazon Comprehend is used for sentiment Analysis on the reviews which are scraped for every 30 min from Trust pilot 
                bitcoin""")

                st.markdown(
                    """
                <span style="color:green"> </span>
                """,
                    unsafe_allow_html=True)


            else:
                st.write('Please login with credentials')

    if choice == "Crypto Currency Dashboard":
        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                st.subheader('Crypto data:')
                st.sidebar.write("## Guide")
                st.sidebar.write("""
                   - select coin(s) you would like data for
                   - select a range of dates 
                   """)

                st.sidebar.write("## Info")
                st.sidebar.write("""
                   - Plot shows the closing price for the day
                   - Plot2 Shows the Open,Close,High,Low
                   - Plot3 shows the Moving Average 
                   """)

                ticker = st.multiselect('Check the cryptos you want to watch',
                                        ['BTC-USD', 'ETH-USD', 'ETC-USD', 'XRP-USD', 'LTC-USD',
                                         'ATOM', 'LINK-USD', 'ALGO-USD', 'OMG-USD'],
                                        default=["ETH-USD"])

                date_picker = st.date_input('Choose Date Range',
                                            [dt.date.today() - dt.timedelta(days=30), dt.date.today() + dt.timedelta(days=1)],
                                            min_value=dt.date.today() - dt.timedelta(days=365),
                                            max_value=dt.date.today() + dt.timedelta(days=1))
                time.sleep(2)
                date_list = []
                increment_date = date_picker[1]
                while increment_date != date_picker[0]:
                    increment_date -= dt.timedelta(days=1)
                    date_list.append(increment_date)
                print(date_list)

                coin_list = []
                for coin in ticker:
                    coin_list.append(coin)

                #################### if 2 coins are selected
                if len(coin_list) != 0:
                    if len(date_list) != 0:
                        datanew = yf.download(tickers=ticker, start=date_picker[0], end=date_picker[1])
                        st.write(datanew)

                        ###################radio Button selection for values
                        genre = st.radio(
                            "Select to see Trend of Values",
                            ('Close', 'Open', 'High'))
                        if genre == 'Close':
                            st.write('You selected Closing Values.')
                        st.subheader('Closing values for selected timeframe')
                        st.line_chart(datanew["Close"])

                        if genre == 'Open':
                            st.write('You selected Open Values.')
                            st.subheader('Opening values for selected timeframe')
                            st.line_chart(datanew["Open"])

                        if genre == 'High':
                            st.write('You selected High Values.')
                            st.subheader('High values for selected timeframe')
                            st.line_chart(datanew["High"])

                        ####################################### if one coin is selected
                        if len(coin_list) == 1:
                            first_value = datanew.Close.iloc[0]
                            last_value = datanew.Close.iloc[-1]
                            change = (last_value - first_value) / first_value
                            if change > 0:
                                st.write("This stock was up {:.2f}".format(change) + '%')
                            elif change < 0:
                                st.write("This Crypto was down by {:.2f}".format(change) + '%')

                            fig = go.Figure()
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['Open'], name="crypto_open", line_color='crimson'))
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['Close'], name="crypto_close", line_color='dimgray'))
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['High'], name="crypto_high", line_color='blueviolet'))
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['Low'], name="crypto_low", line_color='darksalmon'))

                            fig.layout.update(title_text='Crypto Price with Range slider', xaxis_rangeslider_visible=True)
                            st.subheader('Market Summary for selected timeframe')
                            st.write('\n')
                            st.plotly_chart(fig)

                            avg_20 = datanew.Close.rolling(window=20, min_periods=1).mean()
                            avg_50 = datanew.Close.rolling(window=50, min_periods=1).mean()
                            avg_200 = datanew.Close.rolling(window=200, min_periods=1).mean()
                            set1 = {'x': datanew.index, 'open': datanew.Open, 'close': datanew.Close, 'high': datanew.High,
                                    'low': datanew.Low,
                                    'type': 'candlestick', }
                            set2 = {'x': datanew.index, 'y': avg_20, 'type': 'scatter', 'mode': 'lines',
                                    'line': {'width': 1, 'color': 'blue'}, 'name': 'MA 20 periods'}
                            set3 = {'x': datanew.index, 'y': avg_50, 'type': 'scatter', 'mode': 'lines',
                                    'line': {'width': 1, 'color': 'yellow'}, 'name': 'MA 50 periods'}
                            set4 = {'x': datanew.index, 'y': avg_200, 'type': 'scatter', 'mode': 'lines',
                                    'line': {'width': 1, 'color': 'black'}, 'name': 'MA 200 periods'}

                            data = [set1, set2, set3, set4]
                            fig = go.Figure(data=data)
                            st.subheader('Simple Moving Avgerage(SMA)')
                            st.plotly_chart(fig)

                        with st.beta_expander('Show more info'):
                            # Rate of Change
                            st.subheader('Rate of Change over period of time')
                            ROC = ((datanew['Close'] - datanew['Close'].shift(10)) / (
                                datanew['Close'].shift(10))) * 100
                            st.line_chart(ROC)

                else:
                    st.write("### Please select a cryto")
            else:
                st.write('Please login with credentials')

    if choice == 'Logout':
        authValueFlag = False
        f = open('AuthenticationValue.txt', 'a')
        f.truncate(0)
        f.write(str(authValueFlag))
        f.close()
        st.info("You have been logged out!")

    if choice == "Bitcoin Prediction":
        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                b = BtcConverter()
                c = CurrencyCodes()  # force_decimal=True to get Decimal rates

                st.title("Forecast Bitcoin 💰 📈 📉 ")
                col2, col3 = st.beta_columns((2, 1))

                st.sidebar.title("**Currency Converter**")
                choice = st.sidebar.selectbox("Select Currency to convert Bitcoin Price", (
                    'EUR - Euro Member Countries', 'IDR - Indonesia Rupiah', 'BGN - Bulgaria Lev', 'ILS - Israel Shekel',
                    'GBP - United Kingdom Pound', 'DKK - Denmark Krone', 'CAD - Canada Dollar', 'JPY - Japan Yen',
                    'HUF - Hungary Forint', 'RON - Romania New Leu', 'MYR - Malaysia Ringgit', 'SEK - Sweden Krona',
                    'SGD - Singapore Dollar', 'HKD - Hong Kong Dollar', 'AUD - Australia Dollar', 'CHF - Switzerland Franc',
                    'KRW - Korea (South) Won', 'CNY - China Yuan Renminbi', 'TRY - Turkey Lira', 'HRK - Croatia Kuna',
                    'NZD - New Zealand Dollar', 'THB - Thailand Baht', 'USD - United States Dollar', 'NOK - Norway Krone',
                    'RUB - Russia Ruble', 'INR - India Rupee', 'MXN - Mexico Peso', 'CZK - Czech Republic Koruna',
                    'BRL - Brazil Real', 'PLN - Poland Zloty', 'PHP - Philippines Peso', 'ZAR - South Africa Rand'))

                amt = (b.get_latest_price(choice[:3]))
                sym = (c.get_symbol(choice[:3]))
                st.sidebar.write("_Current price of BTC in ", choice[:3], " is", sym, " _", "{:.2f}".format(amt))

                data = yf.download(tickers='BTC-USD', period='1d', interval='1m')

                today_dt = data.iloc[-1:].index[0]
                st.write("**Todays Date:** ", today_dt.strftime('%d %B %Y'))

                closing_price = data.iloc[-1:]['Close'][0]
                st.write("**Closing Price** ${:.2f}".format(closing_price), " **Current Price** ${:.2f}".format(b.get_latest_price('USD')))

                with st.spinner('Loading predictions...'):
                    # Connect to Boto3
                    s3 = boto3.resource(
                        service_name='s3',
                        region_name='us-east-2')
                    bucket_name = 'bitcoin-prediction'
                    filename = 'sagemaker/bitcoin_2018-3-1_2021-4-28.csv'

                    pred = requests.get('https://58jmyxbog3.execute-api.us-east-2.amazonaws.com/test/predictions')
                    data = pred.json()
                    pred_body = data['Predictions']
                    predictions = json.loads(pred_body)
                    df = pd.DataFrame(predictions, columns=['date', 'Predictions'])
                    df.columns = ['Date', 'Predictions']
                    df2 = df.copy()
                    # df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

                    # df = df.set_index('Date')
                    df['Predictions'] = df['Predictions'].astype(float)
                    df['Predictions'] = df['Predictions'].round(2)

                    st.dataframe(df)
                    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
                    df = df.set_index('Date')
                    st.subheader("Forecast for 30 days ")
                    st.line_chart(df['Predictions'])

                    def filedownload(df):
                        csv = df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
                        href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download File</a>'
                        return href

                    st.markdown(filedownload(df), unsafe_allow_html=True)

                    s3 = boto3.client('s3',
                                      region_name='us-east-2')
                                      # aws_access_key_id='AKIAWKCAZTNP6OC5P2VD',
                                      # aws_secret_access_key='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')

                    obj = s3.get_object(Bucket=bucket_name, Key=filename)
                    df1 = pd.read_csv(obj['Body'])
                    # df1 = pd.read_csv('bitcoin_2018-3-1_2021-4-28.csv')
                    df1['Date'] = pd.to_datetime(df1['Date'], format='%b-%d-%Y')
                    df1.sort_values(by='Date', inplace=True)
                    df1 = df1.reset_index()['Close']
                    df = df.reset_index()['Predictions']

                    st.subheader("Overall trend ")
                    chart = st.line_chart(df1)
                    df3 = df1.tolist()
                    df3.extend(df)
                    chart.add_rows(df3[1100:])
            else:
                st.write('Please login with credentials')

    if choice == "Sentiment Analysis":
        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                st.header("Sentiment Analysis on Bitcoin Reviews 💰 ")
                st.subheader('Today\'s Sentiment ')

                # if st.button('GET'):
                with st.spinner('Loading graphs...'):
                    time.sleep(3)

                # today sentiments
                sentiment_td = requests.get('https://58jmyxbog3.execute-api.us-east-2.amazonaws.com/test/todaySentiment')

                data_today = sentiment_td.json()
                sentiment_today = json.loads(data_today['Sentiments'])
                print(sentiment_today)

                df1 = pd.DataFrame(sentiment_today, columns=['date', 'review', 'sentiment'])
                df1['date'] = pd.to_datetime(df1['date']).dt.date
                print('today sentiment', df1)

                sentiment_count = df1["sentiment"].value_counts()
                sentiment_count = pd.DataFrame({"Sentiment": sentiment_count.index, "Reviews": sentiment_count.values})

                # if str(sentiment_count['Sentiment'].values) == 'POSITIVE':
                #     st.write("Considering todays trend of review, its Bearish 📉 ")
                # else:
                st.write("_Considering todays trend of review, its_ ",
                             str(sentiment_count['Sentiment'].values).replace("]", "").replace('[', ""))

                # All sentiments
                sentiment = requests.get('https://58jmyxbog3.execute-api.us-east-2.amazonaws.com/test/allSentiments')

                data = sentiment.json()
                sentiment = json.loads(data['Sentiments'])

                df = pd.DataFrame(sentiment, columns=['date', 'sentiments'])
                df['date'] = pd.to_datetime(df['date']).dt.date
                print(df['date'])

                st.subheader('Overall Sentiment Analysis:')
                date = st.radio(
                    "Select duration of days to check sentiment variations",
                    ('Today', '2 Days', '5 Days', '1 Week'))

                DAYS = 30

                if date == 'Today':
                    DAYS = 1

                if date == '2 Days':
                    DAYS = 2

                if date == '5 Days':
                    DAYS = 5

                if date == '1 Week':
                    DAYS = 7

                days = DAYS
                cutoff_date = dt.date.today() - pd.Timedelta(days=days)
                print(cutoff_date)
                df2 = df[df['date'] > cutoff_date]
                print(df2)
                sentiment_count = df2["sentiments"].value_counts()
                sentiment_count = pd.DataFrame({"Sentiment": sentiment_count.index, "Reviews": sentiment_count.values})
                st.subheader("Number of Reviews by Sentiment")
                fig = px.bar(sentiment_count, x="Sentiment", y="Reviews", color="Reviews")
                st.plotly_chart(fig)
                fig = px.pie(sentiment_count, names=sentiment_count["Sentiment"], values=sentiment_count["Reviews"],
                                         color=sentiment_count["Sentiment"])
                st.plotly_chart(fig)

                symbol = st.sidebar.text_input("Symbol", value='BTC', max_chars=5)

                r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

                data = r.json()

                for message in data['messages']:
                    st.image(message['user']['avatar_url'])
                    st.write(message['user']['username'])
                    st.write(message['created_at'])
                    st.write(message['body'])
            else:
                st.write('Please login with credentials')



if __name__ == '__main__':
    main()
