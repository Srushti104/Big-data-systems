# CSYE 7245 - Bitcoin Price Prediction and Sentiment Analysis Pipeline

### Team Members
Srushti Dhamangaonkar       
Gnana tej Cherukuru

## Table of Contents

### Introduction    
As part of academic project for course CSYE 7245-Big Data Systems & Intelligence Analytics we have built an application on streamlit to predict bitcoin price

### Setup
The pipeline requires an Amazon Web Services account to deploy and run.   
The pipeline uses the folllowing AWS Services:

Lambda
S3.   
DynamoDB.   
Comprehend.   
CloudWatch.  
EC2.   
Cognito.  
SQS.  
IAM

### Requirements    

Python 3.7    
FastAPI.   
Streamlit.   
Postman.   

### Scraping website 
[Bitcoin Price](https://coincodex.com/crypto/bitcoin/).  
[Bitoin Review](https://www.trustpilot.com/review/bitcoin.com)

### Architecture 
Bitcoin Architecture![image](https://user-images.githubusercontent.com/59776740/116674003-16ded400-a972-11eb-9f15-82ce288522d4.png)

#### Part 1: Lambda Functions:

We have to sets of lambda functions one to scrape the price data and the second one to scrape and store the sentiments of reviews from the website:

**Producer-price:**
Triggered by cloud watch to run on an everyday basis to scrape the latest price and merge the data into DynamoDB to ensure uniqueness and then send to SQS instance

**Consure-price:**
Receives the message and processes the data as per requirement and saves it as a .CSV file on S3 bucket 

**Producer-text:**
Triggered by cloud watch to run more frequently to scrape the latest reviews and merge the data into DynamoDB to ensure uniqueness and then send to SQS instance 

**Consumer-text:**
Receives the data and performs sentiment analysis using AWS comprehend and stores the data as .CSV file on S3 bucket  

IAM role to create Lambda functions:

AmazonS3 full access
AmazonDynamoDb full access
ComprehendFullAccess
AWSLambdaExecute

#### Part 2: LSTM(Long Short term memory) Model and AWS Comprehend
LSTM:

For training the model we used LSTM. We created the features using previous 3 years of prices for Open, High, Low, and close price to predict the next 30 days price.

Sentiment Analysis:
Amazon Comprehend is a natural-language processing (NLP) service that uses machine learning to uncover information in unstructured data

Used AWS Comprehend to perform sentiment analysis on the reviews scared which is used in the Stream lit application to aggregate the sentiments based on the dates provided 

#### Fast API:
Built Lambda function with AWS API gateway as trigger to generate 3 API endpoints which communicate with the S3 bucket and the stremlit application  	

#### Part 3: Streamlit
Built a Streamlit application which is hosted on EC2 instance and available for the user to access

#### Features of the Application:

**Bitcoin Prediction** 

- Predicted price of the Bitcoin for the next 30 days 
- Live Bitcoin Price 
- A trend chart showing the trend of the bitcoin over the course of time 

**Cryptocurrency dashboard:**
- Crypto currency prices based on date range selected 
- Trend chart showing the all the Market values 
- Plotly chart showing SMA(Simple Moving Average) of the crypto
- Chart showing ROC(Rate of change) of Crypto

**Sentiment Analysis:**
- Bar chart summarizing the Sentiments of the scraped data over the last week 
- Aggregation of sentiments on today reviews
- Live reviews on Bitcoin feed 

**Login:**
- Secured the application using amazon Cognito
- Only authorised users can login

#### Part 4:Deployment on EC2





