# Introduction

In this assignment, we build an Airflow pipeline for preprocessing and ingesting the Stock data into Snowflake using Snowflake Connector. To access the data, we are designing and building authentication enabled API, while performing unit testing on the API and evaluating the API performance by executing stress testing.  

About the [stock dataset](https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs), it has full historical daily price and volume data for all US-based stocks and ETFs trading on the NYSE, NASDAQ, and NYSE MKT. The data is presented in CSV format as follows: Date, Open, High, Low, Close, Volume, OpenInt. 

## Requirements
  * Python 3.7
  * SnowFlake Account
  * Sql connector
  * FastAPI
  * Locust
  * pytest
  * Airflow
  * Postman

## Configuration:  
Install Snowflake- Connector.   
```pip install --upgrade snowflake-connector-python```     
  
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

Airflow.  
```pip install -r requirements.txt ```   

## Data Ingestion pipeline
  * Add columns to identify ETF and stock and merge the data in one csv file
  * Upload the csv to snowflake by creating staging area

## Running above pipelines in Airflow:
 Once installations are completed, configure Airflow by running:
 

Use your present working directory as the airflow home
```
export AIRFLOW_HOME=~(pwd)
```

Export Python Path to allow use of custom modules by Airflow
```
export PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"
```
Initialize the database
```
airflow db init 


airflow users create \
    --username admin \
    --firstname <YourName> \
    --lastname <YourLastName> \
    --role Admin \
    --email example@example.com
```
Start the Airflow server in daemon
```
airflow webserver -D
```
Start the Airflow Scheduler
```airflow scheduler```

Once both are running - you should be able to access the Airflow UI by visiting http://127.0.0.1:8080/home on your browser.

To kill the Airflow webserver daemon:
```lsof -i tcp:8080  ```

``` 
COMMAND   PID        USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  33911 akshaybhoge    6u  IPv4 0x5618802e5591d6b1      0t0  TCP *:http-alt (LISTEN)
Python  91569 akshaybhoge    6u  IPv4 0x5618802e5591d6b1      0t0  TCP *:http-alt (LISTEN)
Python  91636 akshaybhoge    6u  IPv4 0x5618802e5591d6b1      0t0  TCP *:http-alt (LISTEN)
Python  91699 akshaybhoge    6u  IPv4 0x5618802e5591d6b1      0t0  TCP *:http-alt (LISTEN)
Python  91743 akshaybhoge    6u  IPv4 0x5618802e5591d6b1      0t0  TCP *:http-alt (LISTEN) 
```

Kill the process by running kill <PID> - in this case, it would be ```kill 33911```

 
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
Assignment 3/
├── config/ 
│   └── config.py - snowflake config file
├── dags/
│   └── ingestion_pipeline.py - ingestion pipeleine dag
├── data/
│   ├── ETFs/ ETF file folder
│   │   ├── .DS_Store
│   │   ├── aadr.us.txt
│   │   ├── aaxj.us.txt
│   │   └── acim.us.txt
│   └── Stocks/ - Stock file folder
│       ├── .DS_Store
│       └── a.us.txt
├── diagram/ - flow diagram using Diagrams
│   ├── creditedge_api.png
│   ├── moodys_api.png
│   ├── sample_moodys.py
│   ├── stock_api.png - StockAPI diagram
│   └── StockAPI.py - script to generate diagram
├── ingest_db.py - script to ingest data to snowflake
├── locust_test/ - folder with locust test scripts
│   ├── locust_company.py - script to load test api with company name
│   ├── locust_date.py - script to load test api with date name
│   └── locust_year.py - script to load test api with year name
├── merge_files.py - merge ETF and Stock files
├── notebook/
│   └── StockAPI_testing.ipynb - notebook with unit testing using pytest
├── README.md
├── requirements.txt - airflow requirement
├── stockAPI.py - FatsAPI script to query snowflake
└── test_stockAPI.py 
```

## Codelab Document:   
For more information refer the [document](https://codelabs-preview.appspot.com/?file_id=1iF3m30Fu3eYKeD1B-BLeWZ6l2DBuktPcaK2GFXMrWUQ#0)
