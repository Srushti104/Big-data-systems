import streamlit as st
import datetime as dt
import plotly.graph_objects as go
import time
import boto3
import yfinance as yf


global authValueFlag
authValueFlag = False
currentFunction =""



def main():

    menu = ['Login','Home','Architecture',"Crypto Currency Dashboard", 'Bitcoin Prediction', 'Sentiment Analysis','Logout']
    choice = st.sidebar.selectbox("Menu", menu)

    st.markdown('<style>body{background-color: #FFF2C2;}</style>', unsafe_allow_html=True)
    st.title("""
       Crypto Currency Dashboard
       """)

    if choice == "Login":
        usrname = st.text_input('Username')
        password = st.text_input('Password',type="password")
        email = st.text_input('Email')
        if st.button('Login'):
            f = open('AuthenticationValue.txt', 'a')
            f.truncate(0)
            current = open('Functionlocation.txt','a')
            current.truncate(0)
            try:
                aws_client = boto3.client('cognito-idp',
                                          region_name='us-east-2'
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
                st.balloons()
                authValueFlag = True
            f = open('AuthenticationValue.txt', 'a')
            f.truncate(0)
            f.write(str(authValueFlag))
            f.close()


    if choice == "Home":

        f = open('AuthenticationValue.txt', 'r')
        for line in f:
            if line=='True':
                st.image('https://s27389.pcdn.co/wp-content/uploads/2021/03/bitcoin-hits-all-time-high-of-61000-is-regulation-needed-1013x440.jpeg')
                st.subheader('About:')
                st.write('A cryptocurrency, broadly defined, is currency that takes the form of tokens or “coins” and exists on a distributed and decentralized ledger.Bitcoin continues to lead the pack of cryptocurrencies in terms of market capitalization, user base, and popularity.')
                st.subheader('Content:')
                st.write("""
                           - Crypto Currencies Market value between selected time frame 
                           - An efficient Predictive model to forecast future trends for Bitcoin Market for the next 30 days
                           - Sentiment analysis on User reviews to detect possible correlations with the price of cryptocurrencies and digital tokens
                           - Technical indicators and Features such as Rate Of Change(ROC), Simple Moving Average, Exponential Moving Average
                           """)
                st.subheader('Machine Leanring Model:')
                st.write("""
                            - We used LSTM(Long Short term Memory Model) frequently used for time series modeling. 
                            - Trained the LSTM model on data scraped from Coin Index using features Open, High,Low and Close
                            - Trained the model on 3 years to predict the Bitcoin price for next 30 days
                            - Amazon Comprehend is used for sentiment Analysis on the reviews which are scraped for every 30 min from Trust pilot bitcoin
                                           """)



                st.markdown(
                """
                <span style="color:green"> </span>
                """,
                unsafe_allow_html=True)
            else:
                st.write('Please login with credentials')




    if choice == "Crypto Currency Dashboard":

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
                                                                   ['BTC-USD', 'ETH-USD', 'ETC-USD', 'XRP-USD', 'LTC-USD', 'ATOM', 'LINK-USD', 'ALGO-USD', 'OMG-USD','DOGE-USD'],default=["ETH-USD"])

        date_picker = st.date_input('Choose Date Range',
                                                              [dt.date.today() - dt.timedelta(days=30), dt.date.today() + dt.timedelta(days=1)],
                                                              min_value=dt.date.today() - dt.timedelta(days=365),
                                                               max_value=dt.date.today() + dt.timedelta(days=1))
        time.sleep(5)
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
            if len(date_list) !=0:
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
                #increment in crypto price caluculation
                    first_value = datanew.Close.iloc[0]
                    last_value = datanew.Close.iloc[-1]
                    change = (last_value - first_value) / first_value
                    if change > 0:
                        st.write("This Crypto was up by {:.2f}".format(change) + '%')
                    elif change < 0:
                        st.write("This Crypto was down by {:.2f}".format(change) + '%')


                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=datanew.index, y=datanew['Open'], name="crypto_open", line_color='crimson'))
                    fig.add_trace(go.Scatter(x=datanew.index, y=datanew['Close'], name="crypto_close", line_color='dimgray'))
                    fig.add_trace(go.Scatter(x=datanew.index, y=datanew['High'], name="crypto_high", line_color='blueviolet'))
                    fig.add_trace(go.Scatter(x=datanew.index, y=datanew['Low'], name="crypto_low", line_color='darksalmon'))

                    fig.layout.update(title_text='Crypto Price with Rangeslider', xaxis_rangeslider_visible=True)
                    st.subheader('Market Summary for selected timeframe')
                    st.write('\n')
                    st.plotly_chart(fig)

                    avg_20 = datanew.Close.rolling(window=20, min_periods=1).mean()
                    avg_50 = datanew.Close.rolling(window=50, min_periods=1).mean()
                    avg_200 = datanew.Close.rolling(window=200, min_periods=1).mean()
                    set1 = {'x': datanew.index, 'open': datanew.Open, 'close': datanew.Close, 'high': datanew.High, 'low': datanew.Low,
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

    if choice=='Logout':
        authValueFlag = False
        f = open('AuthenticationValue.txt', 'a')
        f.truncate(0)
        f.write(str(authValueFlag))
        f.close()
        st.write("You have been Logged out")



if __name__ == '__main__':
    main()


