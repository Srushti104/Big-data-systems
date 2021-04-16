# Introduction

**Part 1:**
The goal of this assignment is to create API that Anonmyizes the data through: 
 - Masking
 - Anonymization

**Part 2:** 
Goal is to deploy a sentiment analysis model to create a Model-as-a-service for anonymized data using dockerised TFX servinf model Albert.
Eventually builidng Streamlit app to host all the API and dockerised sentiment analysis model.


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
 

 




 
## Running FastAPI 
```uvicorn main:app --reload```   

### API Documentation  
http://127.0.0.1:8000/docs


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
 
## Tensorflow serving

TensorFlow models using TensorFlow Extended (TFX)![image](https://user-images.githubusercontent.com/59776740/114988710-a067af80-9e64-11eb-99d8-1804235333f8.png)

Download the TensorFlow Serving Docker image and repo
```
docker pull tensorflow/serving

git clone https://github.com/tensorflow/serving
```
Start TensorFlow Serving container and open the REST API port
```
docker run -t --rm -p 8501:8501 -v "/Users/akshaybhoge/PycharmProjects/Assignment4/albert_exported_model/9:/models/saved_model" -e MODEL_NAME=saved_model tensorflow/serving &
```
 
## Project Structure:

```
Assignment 4/
├── albert_exported_model/ - Folder with saved albert model
│   ├── 9/
│   │   ├── assets/
│   │   │   └── 30k-clean.model
│   │   ├── saved_model.pb - Albert exported model
│   │   └── variables/
│   │       ├── variables.data-00000-of-00001
│   │       └── variables.index
│   └── dynamo.py 
├── api.py - FastApi script
├── app.py - Streamlit app
├── inference/
│   ├── Dockerfile - docker file
│   └── main.py - 
├── locust/
│   └── locustfile.py - locust file for load testing
├── README.md
├── test_edgar.py
├── test_inference.py
└── TFX_Pipeline_for_AlBert_Preprocessing.ipynb - notebook for training Albert model on IMDB

```

## Codelab Document:   
For more information refer the [document](https://codelabs-preview.appspot.com/?file_id=1F0GC-J0CQc6fa3UfzZ91Dgre0IbgdxhG4zWrbsCfJtE#0)
