import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import time
#from crypto_coin import Coin
#import data_plot
import boto3
import datetime
import yfinance as yf
import matplotlib.pyplot as plt

ACCESS_KEY='AKIAWKCAZTNP6OC5P2VD'
SECRET_KEY='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'






def main():

    menu = ['Home','Architecture',"Crypto Currency Dashboard", 'Bitcoin Prediction', 'Sentiment Analysis']
    choice = st.sidebar.selectbox("Menu", menu)

    st.markdown('<style>body{background-color: #FFF2C2;}</style>', unsafe_allow_html=True)

    # st.sidebar.write("## Guide")
    # st.sidebar.write("""
    # - select coin(s) you would like data for
    # - select the currency you wish to use
    # - select a range of dates (this is for the candle stick plot)
    # """)
    #
    # st.sidebar.write("## Info")
    # st.sidebar.write("""
    # - candle stick plot(s) -- default date range is last 30 days
    # - 24 hour stats for the selected coins(s)
    # - the order book for the selected coin(s)
    # - the ticker for the selected coin(s)
    # """)

    st.title("""
       Crypto Currency Dashboard
       """)

    if choice == "Home":
        st.subheader('About:')
        st.write('Bitcoin is a digital currency and a payment system invented by an unknown group or person by the name Satoshi Nakamoto , who published the invention in 2008 and released it as open source software in 2009. It is the first decentralized digital currency, meaning the system works without a single administrator or central bank, you can use them in every country, your account cannot be frozen, and there are no prerequisites or limits .')
        st.markdown(
            """
            <span style="color:green"> </span>
            """,
            unsafe_allow_html=True)

        if st.button('Documentation'):
            st.write(
                f'<iframe src="http://127.0.0.1:8000/sentiment", width=850, height=600  , scrolling=True></iframe>',
                unsafe_allow_html=True,
            )


    if choice == "Crypto Currency Dashboard":

        st.subheader('Bitcoin data:')
        st.sidebar.write("## Guide")
        st.sidebar.write("""
           - select coin(s) you would like data for
           - select a range of dates 
           """)

        st.sidebar.write("## Info")
        st.sidebar.write("""
           - candle stick plot(s) -- default date range is last 30 days
           - 24 hour stats for the selected coins(s)
           - the order book for the selected coin(s)
           - the ticker for the selected coin(s)
           """)

        ticker = st.multiselect('Check the cryptos you want to watch',
                                                                   ['BTC-USD', 'ETH-USD', 'ETC-USD', 'XRP-USD', 'LTC-USD', 'ATOM', 'LINK-USD', 'ALGO-USD', 'OMG-USD'],default=["ETH-USD"])

        date_picker = st.date_input('Choose Date Range',
                                                              [dt.date.today() - dt.timedelta(days=30), dt.date.today() + dt.timedelta(days=1)],
                                                              min_value=dt.date.today() - dt.timedelta(days=365),
                                                               max_value=dt.date.today() + dt.timedelta(days=1))
        time.sleep(4)
        date_list = []
        increment_date = date_picker[1]
        while increment_date != date_picker[0]:
            increment_date -= dt.timedelta(days=1)
            date_list.append(increment_date)
        print(date_list)

        coin_list = []
        for coin in ticker:
            coin_list.append(coin)

        if len(coin_list) != 0:
            if len(date_list) !=0:
                datanew = yf.download(tickers=ticker, start=date_picker[0], end=date_picker[1])
                st.write(datanew)

                st.subheader('Closing values for selected timeframe')
                st.line_chart(datanew["Close"])

                if len(coin_list) == 1:
                    first_value = datanew.Close.iloc[0]
                    last_value = datanew.Close.iloc[-1]
                    change = (last_value - first_value) / first_value
                    if change > 0:
                        st.write("This stock was up {:.2f}".format(change) + '%')
                    elif change < 0:
                        st.write("This stock was down {:.2f}".format(change) + '%')

        else:
            st.write("### Please select a cryto")









if __name__ == '__main__':
    main()


