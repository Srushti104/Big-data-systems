# Introduction

##  Model-as-a-service
In this assignment, we build an Airflow pipeline for preprocessing and ingesting the Stock data into Snowflake using Snowflake Connector. To access the data, we are designing and building authentication enabled API, while performing unit testing on the API and evaluating the API performance by executing stress testing.  

About the [stock dataset](https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs), it has full historical daily price and volume data for all US-based stocks and ETFs trading on the NYSE, NASDAQ, and NYSE MKT. The data is presented in CSV format as follows: Date, Open, High, Low, Close, Volume, OpenInt. 

## Requirements
  * Python 3.7
  * AWS Cognito, Lambda, S3, DynamoDB, Comprehend
  * Albert using Tensorflow Extended (TFX)
  * REST API
  * FastAPI
  * Locust
  * pytest
  * Docker
  * Postman
  * Streamlit

## Configuration:  
Install Streamlit.   
```pip install streamlit```     
  
FastAPI    
```pip3 install fastapi```      
```pip3 install uvicorn```   
```pip3 install iexfinance```      

Pytest from Jupyter Notebook   
```pip install pytest```   
```pip install -U ipytest```   
```pip install pytest-tornasync```  
```pip install nest_asyncio```    
```pip install ipynb```   
 
Locust.  
```pip install locust```
  

## API 1: Access
  * Retrieve the EDGAR filings data from the S3 bucket
  
## API 2: Named entity recognition
  * Call Amazon Comprehend to find entities.
  * Store these on S3
 
## API 3: Implement masking, and anonymization functions
  * indicate which entities need to be masked, which needs to be anonymized
  * store back the anonymized adn masked file on S3
 

 




 
## Rnning FastAPI 
```uvicorn main:app --reload```   

### API Documentation  
http://127.0.0.1:8000/docs

**Authentication key**: '1234567asdfgh'

## Running Locust

Put the above code in a file named locustfile.py in your current directory and run:   

```locust```     

If your Locust file is located somewhere else, you can specify it using -f 
 
```locust -f locust_files/my_locust_file.py```     

### Locust’s web interface.  
Once you’ve started Locust using one of the above command lines, you should open up a browser and point it to http://127.0.0.1:8089     

## Running pytest    
Confirm the correct version:  
```pytest --version ```  
  
Execute the test function:    
``` pytest```   
 
## Project Structure:

```
Assignment 4/

```

## Codelab Document:   
For more information refer the [document]()
