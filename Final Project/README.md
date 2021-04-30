# CSYE 7245 - Bitcoin Price Prediction and Sentiment Analysis Pipeline

### Team Members
Srushti Dhamangaonkar       
Gnana tej Cherukuru

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

### Scraping website 
[Bitcoin Price](https://coincodex.com/crypto/bitcoin/).  
[Bitoin Review](https://www.trustpilot.com/review/bitcoin.com)

### Streamlit hosted on EC2 
Link: http://3.16.82.118:8501/

### Architecture 
Bitcoin Architecture![image](https://user-images.githubusercontent.com/59776740/116674003-16ded400-a972-11eb-9f15-82ce288522d4.png)

### Setup
Clone this repo to your local machine using ```https://github.com/Srushti104/Team1_CSYE7245_Spring2021.git```

#### Requirements    
Python 3.7    
FastAPI.   
Streamlit.   
Postman.   

```pip3 install -r requirements.txt```

##### Configuration.   
FastAPI     
```pip3 install fastapi```  
```pip3 install uvicorn```   
```pip3 install iexfinance```  


#### Lambda Deployment:

* After cloning the repo and installing the required pacakages zip all the installed libraires. Move the lambda scripts to the zip folder.
* Upload the zip folder to the s3 bucket and make a note of the object URL
* Create associated lambda fucntions with IAM role of lambda ececute having policies of AWS S3full access,DynamoDB full access, ComprehendfullAccess, SQSfull access
* Upload the zip folder rmo s3 location to Lambda
* Once the lambda's are deployed make sure to check the configuration to avoid timeout error. 
* Create an SQS queue which acts as a trigger to your consumer Lambdas.


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
For training the model we used LSTM. We created the features using previous 3 years of prices for Open, High, Low, and close price to predict the next 30 days price.

Sentiment Analysis:
Amazon Comprehend is a natural-language processing (NLP) service that uses machine learning to uncover information in unstructured data

Used AWS Comprehend to perform sentiment analysis on the reviews scared which is used in the Stream lit application to aggregate the sentiments based on the dates provided 

#### Fast API:
Built Lambda function with AWS API gateway as trigger to generate 3 API endpoints which communicate with the S3 bucket and the streamlit application  	

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
* Setting up the Amazon Instance
- Go to AWS Management Console using https://us-west-2.console.aws.amazon.com/console.
- On the AWS Management Console, you can select “Launch a Virtual Machine”. 
- Select the 18.04 Ubuntu Server since it is applicable for the Free Tier.
- Git the Public DNS(IPv4) Address and the ```streamlit.pem``` file. 
- run below command

```
chmod 400 streamlit.pem
ssh -i "streamlit.pem" ubuntu@<Your Public DNS(IPv4) Address>
```

Install all the required packages.
```
git clone https://github.com/Srushti104/Team1_CSYE7245_Spring2021.git
cd Team1_CSYE7245_Spring2021/Final Project/
streamlit run crypto.py
```
Now you can go to a browser and type the external URL to access your app.


### Project Structure

```
Final Project/
├── .streamlit/ - 
│   └── config.toml - streamlit theme config
├── api.py - Fast API script
├── crypto.py - Streamlit app
├── Lambda/
│   ├── everydaysentiment.py - gets all the review from dynamo to s3 (scheduled everyday once)
│   ├── reviews_s3new.py - gets latest review from dynamo to s3, linked to SQS
│   ├── reviewscrape_latest.py - scrapes reviews from website and stores to dynamodb 
│   ├── sentimentAPI.py - Fast API package
│   ├── test_scrape.py - scrapes bitcoin price from website and store dynamodb
│   └── testdynamo_s3.py - moves bitcoin price from dynamo to s3
├── LSTM/
│   └── lstm_model.py - model training script
├── README.md
└── requirements.txt
```
### Codelab Document:
For more information refer the [document](https://codelabs-preview.appspot.com/?file_id=1juT4LFQtWbYCmqQhZJlFMNsBN9bD3xpbYq-HtJ4QDmg#0)
