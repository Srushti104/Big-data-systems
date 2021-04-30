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

img = Image.open('Images/bitcoin.png')
st.set_page_config(page_title='Crypto Currency Forecast', page_icon=img, layout='centered')

col1, col2, col3 = st.beta_columns((1,3,1))

if authValueFlag == True:
    col3.button('Logout')

def main():
    menu = ['Login', 'Home', 'Architecture', "Crypto Currency Dashboard", 'Sentiment Analysis', 'Bitcoin Prediction']
    st.sidebar.title("** Menu **")
    choice = st.sidebar.selectbox("Select the page from dropdown to browse ", menu)
    col1, col2, col3 = st.beta_columns((1, 3, 1))
    col2.title("**_Crypto Currency Forecast Application_**")

    if choice == "Login":
        #st.subheader("Login ")
        col1, col2, col3 = st.beta_columns((1, 3, 1))
        col2.subheader("Enter your Username and Password:")
        usrname = col2.text_input('Username')
        password = col2.text_input('Password', type="password")
        email = col2.text_input('Email')
        if col2.button('Login'):
            f = open('AuthenticationValue.txt', 'a')
            f.truncate(0)
            current = open('Functionlocation.txt', 'a')
            current.truncate(0)
            try:
                aws_client = boto3.client('cognito-idp', region_name='us-east-2')
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
                col2.info("user created")
                authValueFlag = True
                print(authValueFlag)
            except aws_client.exceptions.UsernameExistsException as e:
                col2.info("Login successfully")

                authValueFlag = True
            f = open('AuthenticationValue.txt', 'a')
            f.truncate(0)
            f.write(str(authValueFlag))
            f.close()

    if choice == "Home":

        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                logout = st.sidebar.button('Logout')
                if logout:
                    authValueFlag = False
                    f = open('AuthenticationValue.txt', 'a')
                    f.truncate(0)
                    f.write(str(authValueFlag))
                    f.close()
                    st.info("You have been logged out!")
                    break
                col1, col2, col3 = st.beta_columns((1, 2, 1))
                img1 = Image.open('Images/bitcoin2.png')
                col2.image(img1)
                st.markdown('---')
                col1, col2, col3, col4 = st.beta_columns((1, 1, 2, 1))
                col2.subheader('About:')
                col3.write('A cryptocurrency, broadly defined, is currency that takes the form of tokens or “coins” and '
                         'exists on a distributed and decentralized ledger.Bitcoin continues to lead the pack of '
                         'cryptocurrencies in terms of market capitalization, user base, and popularity.')
                st.markdown('---')
                col1, col2, col3, col4 = st.beta_columns((1, 1, 2, 1))
                col2.subheader('Content:')
                col3.write("""
                    - Crypto Currencies Market value between selected time frame 
                    - An efficient Predictive model to forecast future trends for Bitcoin Market for the next 30 days
                    - Sentiment analysis on User reviews to detect possible correlations with the price of cryptocurrencies and digital tokens
                    - Technical indicators and Features such as Rate Of Change(ROC), Simple Moving Average, Exponential Moving Average""")
                st.markdown('---')
                col1, col2, col3, col4 = st.beta_columns((1, 1, 2, 1))
                col2.subheader('Machine Learning Model:')
                col3.write("""
                    - We used LSTM(Long Short term Memory Model) frequently used for time series modeling
                    - Trained the LSTM model on data scraped from Coin Index using features Open, High,Low and Close 
                    - Trained the model on 3 years to predict the Bitcoin price for next 30 days 
                    - Amazon Comprehend is used for sentiment Analysis on the reviews which are scraped for every 30 min from Trust pilot bitcoin""")
                st.markdown('---')


            else:
                st.write('Please login with credentials')

    if choice == "Crypto Currency Dashboard":
        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                logout = st.sidebar.button('Logout')
                if logout:
                    authValueFlag = False
                    f = open('AuthenticationValue.txt', 'a')
                    f.truncate(0)
                    f.write(str(authValueFlag))
                    f.close()
                    st.info("You have been logged out!")
                    break

                st.sidebar.write("### Guide")
                st.sidebar.write("""
                    - Select coin(s) from dropdown 
                    - Choose intended date range 
                    """)

                st.sidebar.write("### Info")
                st.sidebar.write("""
                    - The table displays Open, Close, High, Low and volume for each day in selected data range
                    - To View plots for Close, Open, High Values select the radio button.
                    - The Rate of Change over Period of time plot shows how volatile selected Coin(s) is.
                    """)
                st.markdown('---')

                st.write('View the Open, High, Low Close price and Volume of selected Crypto')
                # st.subheader('Select crypto currency:')
                col1,col2 = st.beta_columns((1,4))
                ticker = col1.multiselect('Select crypto currency',
                                        ['BTC-USD', 'ETH-USD', 'ETC-USD', 'XRP-USD', 'LTC-USD',
                                         'ATOM', 'LINK-USD', 'ALGO-USD', 'OMG-USD'],
                                        default=["ETH-USD"])

                date_picker = col1.date_input('Choose Date Range',
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
                        col2.write(datanew)
                        st.markdown('---')
                        c1,c2 = st.beta_columns((1,4))
                        ###################radio Button selection for values
                        c1.subheader('Select the values to see the trend')
                        genre = c1.radio('\n',
                            ('Close', 'Open', 'High'))
                        if genre == 'Close':
                            c1.write('You selected Closing Values.')
                            #c2.subheader('Closing values for selected timeframe')
                            c2.line_chart(datanew["Close"])

                        if genre == 'Open':
                            c1.write('You selected Open Values.')
                            #c2.subheader('Opening values for selected timeframe')
                            c2.line_chart(datanew["Open"])

                        if genre == 'High':
                            c1.write('You selected High Values.')
                            #c2.subheader('High values for selected timeframe')
                            c2.line_chart(datanew["High"])

                        ####################################### if one coin is selected
                        st.markdown('---')
                        st.subheader('Rate of Change over period of time')
                        ROC = ((datanew['Close'] - datanew['Close'].shift(1)) / (
                            datanew['Close'].shift(1))) * 100
                        st.line_chart(ROC)


                        if len(coin_list) == 1:
                            first_value = datanew.Close.iloc[0]
                            last_value = datanew.Close.iloc[-1]
                            change = (last_value - first_value) / first_value
                            if change > 0:
                                st.write(coin, " was up {:.2f}".format(change) + '%')
                            elif change < 0:
                                st.write(coin," was down by {:.2f}".format(change) + '%')
                            st.markdown('---')
                            layout = go.Layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)'
                            )
                            s1,s2=st.beta_columns((2,2))
                            fig = go.Figure(layout=layout)
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['Open'], name="Open", line_color='crimson'))
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['Close'], name="Close", line_color='dimgray'))
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['High'], name="High", line_color='blueviolet'))
                            fig.add_trace(
                                go.Scatter(x=datanew.index, y=datanew['Low'], name="Low", line_color='darksalmon'))

                            s1.subheader('Market Summary for selected timeframe')

                            fig.layout.update(title_text='Check selected crypto currency Price with Range slider',
                                              xaxis_rangeslider_visible=True)
                            s1.plotly_chart(fig)

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
                            fig = go.Figure(data=data, layout=layout)

                            s2.subheader('Simple Moving Avgerage(SMA)')
                            fig.layout.update(title_text='Check Simple Moving Average of selected crypto currency with Range slider',
                                              xaxis_rangeslider_visible=True)
                            s2.plotly_chart(fig)
                            st.markdown('---')

                else:
                    st.write("### Please select a Cryto Currency")
            else:
                st.info('Please login with credentials')

    # if choice == 'Logout':
    #     authValueFlag = False
    #     f = open('AuthenticationValue.txt', 'a')
    #     f.truncate(0)
    #     f.write(str(authValueFlag))
    #     f.close()
    #     st.info("You have been logged out!")

    if choice == "Bitcoin Prediction":
        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                logout = st.sidebar.button('Logout')
                if logout:
                    authValueFlag = False
                    f = open('AuthenticationValue.txt', 'a')
                    f.truncate(0)
                    f.write(str(authValueFlag))
                    f.close()
                    st.info("You have been logged out!")
                    break
                b = BtcConverter()
                c = CurrencyCodes()  # force_decimal=True to get Decimal rates
                st.markdown('---')
                st.subheader("Forecast Bitcoin 💰 📈 📉 ")
                st.sidebar.subheader("**Currency Converter**")
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
                    st.markdown('---')
                    st.subheader("Forecast for 30 days ")
                    st.line_chart(df['Predictions'])

                    def filedownload(df):
                        csv = df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
                        href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download File</a>'
                        return href

                    st.markdown(filedownload(df), unsafe_allow_html=True)
                    st.markdown('---')
                    s3 = boto3.client('s3',
                                      region_name='us-east-2')

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
                    st.markdown('---')
            else:
                st.write('Please login with credentials')

    if choice == "Sentiment Analysis":
        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line == 'True':
                logout = st.sidebar.button('Logout')
                if logout:
                    authValueFlag = False
                    f = open('AuthenticationValue.txt', 'a')
                    f.truncate(0)
                    f.write(str(authValueFlag))
                    f.close()
                    st.info("You have been logged out!")
                    break
                # if st.button('GET'):
                with st.spinner('Loading data...'):
                    time.sleep(3)

                st.markdown('---')
                st.subheader("Sentiment Analysis on Bitcoin Reviews 💰 ")
                b = BtcConverter()
                c = CurrencyCodes()

                # amt = (b.get_latest_price('USD'))
                # sym = (c.get_symbol('USD'))
                # st.write("_Current price of BTC in USD", " is", sym, " _", "{:.2f}".format(amt))
                data = yf.download(tickers='BTC-USD', period='1d', interval='1m')

                today_dt = data.iloc[-1:].index[0]
                st.write("**Todays Date:** ", today_dt.strftime('%d %B %Y'))

                closing_price = data.iloc[-1:]['Close'][0]
                st.write("**Closing Price** ${:.2f}".format(closing_price),
                         " **Current Price** ${:.2f}".format(b.get_latest_price('USD')))

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

                st.sidebar.subheader('Today\'s Sentiment ')
                st.sidebar.write("_Considering todays trend of review, its_ ",
                             str(sentiment_count['Sentiment'].values).replace("]", "").replace('[', ""))

                # All sentiments
                sentiment = requests.get('https://58jmyxbog3.execute-api.us-east-2.amazonaws.com/test/allSentiments')

                data = sentiment.json()
                sentiment = json.loads(data['Sentiments'])

                df = pd.DataFrame(sentiment, columns=['date', 'sentiments'])
                df['date'] = pd.to_datetime(df['date']).dt.date
                print(df['date'])

                st.sidebar.subheader('Overall Sentiment Analysis:')
                date = st.sidebar.radio(
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

                st.markdown('---')

                st.subheader("Sentiment variations for selected range")

                fig = px.bar(sentiment_count, x="Sentiment", y="Reviews", color="Reviews")
                fig.update_layout({
                    'plot_bgcolor':'rgba(0,0,0,0)',
                    'paper_bgcolor':'rgba(0,0,0,0)'}
                )
                st.plotly_chart(fig)
                fig = px.pie(sentiment_count, names=sentiment_count["Sentiment"], values=sentiment_count["Reviews"],
                                         color=sentiment_count["Sentiment"])
                st.plotly_chart(fig)

                # symbol = st.text_input("Search ", value='BTC', max_chars=5)
                r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/BTC.json")
                data = r.json()

                st.subheader("Live Feed of Bitcoin Reviews")
                st.markdown('---')

                for message in data['messages']:
                    col1, col2, col3, col4 = st.beta_columns((1, 1, 2, 1))
                    col2.image(message['user']['avatar_url'])
                    col2.write(message['user']['username'])
                    col2.write(message['created_at'])
                    col3.write(message['body'])
                    st.markdown('---')

            else:
                st.write('Please login with credentials')


if __name__ == '__main__':
    main()
