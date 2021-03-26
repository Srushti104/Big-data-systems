# Introduction:

  In this assignment, we build a sentiment analysis micro service that could take a new Edgar file in json format and generate sentiments for each
  statement in the referenced EDGAR file and store it on S3 bucket.
 
 As part of the assignment, we orchestrated Airflow Pipelines as mentioned below:
 
  * Annotation Pipeline: We built pipeline using Airflow for pre processing and labeling the data using AWS comprehend API 
  * Training Pipeline: We configured the pipeline to train a sentiment analysis model using BERT on saved data
  * Inference Pipeline: We designed the inference pipeline to take new data in json format and get back the predictions from the microservice running on the Docker image
  
 ## Requirements:
  * Python 3.7
  * AWS account - S3 bucket
  * Install Docker 
  * AWS comprehend
  * Airflow 
  * Flask
  * Postman
  * Install the dependencies as outlined in the ```requirements.txt``` by running     
 	 ```pip install -r requirements.txt```

     
 ## Running the Flask Server on Docker Image:

  The objective of the project is to POST the input in JSON format to the flask server running on a docker file 
  which returns the sentiment for the input using the pretrained saved model
  
  To serve the provided pre-trained model, follow these steps:
  
   * git clone this repo
   * cd Assignment2/Bert_model
   * Use the ```docker build -t edgar:latest .```  to create docker image which creates a blueprint of the environment with all the requirements
   * Run ```docker images``` & find the image id of the newly built Docker image
   * To run the docker image -- ```docker run -d --name edgar-container-v1 -p 5050:5050 {image_id}```
     
   If everything worked properly, you should now have a container running, which:
   Spins up a Flask server that accepts POST requests at http://0.0.0.0:5050/predict
   
   To test :
   Write your own POST request (e.g. using [Postman](https://www.postman.com/), here is an example response:
  
  Input JOSN:
  ```{
  	"data": [
		"this workshop is fun", 
		"this workshop is boring"
		]
     }
  ```
  
  Output JSON:
  
  ``` {
    "input": {
        "data": [
            "this workshop is fun",
            "this workshop is boring"
        ]
    },
    "pred": [
        [
            0.9856576323509216      # closer to 1 => positive
        ],
        [
            -0.89903425872325897     # closer to -1 => negative
        ]
    ]
}
```

You can also pass a curl command from the terminal once the Docker image is up and running. 
Example:

   ```curl -i -H "Content-Type: application/json" -X POST -d '{"data": ["this is the best!", "this is the worst!"]}' http://0.0.0.0:5050/predict```
  
### Images on DockerHub.com
edagr-api [Link](https://hub.docker.com/layers/143174921/srushti104/edgar-api/latest/images/sha256-8fda55fd64e9c015c549bef0acacc25538b49bab6715552716f5642235f84488?context=explore)

 * NOTE: Microservices are hosted on port 5050 in docker. Building docker images may take several minute.
   
 ## Annotation Pipeline:
   * Uploading the provided data on s3 bucket 
   * Accessing the data on s3 and preprocess the data into list of sentences using Amazon Comprehend API to label the lines with the sentiment analysis score 
   * Scaling the returned output and storing the data on AWS s3 Bucket

 ## Training Pipeline:
   * Built a configurable pipeline to access the data on s3 bucket, train the model and upload the saved model to s3 bucket 
   * Used the BERTBaseUncased model to train and fine tune on labeled data to predict the sentiment of the data
   * Saving the trained model to s3 bucket in .bin format 
    
## Inference pipeline:
   * The pipeline would dynamically get the file from EDGAR, pre-process the file,create a list of sentences for inference. 
   * Jsonify the sentences and invoke the the flask server running on the docker image 
   * Post the input data and get back the sentiments and Format the output to a csv file and store it to a bucket.

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

## Project Structure:
```
Assignment 2/ - root folder
├── annotation/ - folder with annotation pipeline script to label data
│   ├── csv_s3_upload.py - 
│   ├── edgar_sentiment_analysis.py - cleaning and preprocessing text file
│   ├── s3_upload.py - upload company earnings transcripts to S3
│   └── scaling.py - invoke AWS comprehend to get sentiment for each sentence
├── BERT_model/ - folder with model training scripts
│   ├── app.py - flask app
│   ├── config.py - config file
│   ├── dataset.py - set up dataset
│   ├── Dockerfile - Docker file
│   ├── engine.py - train and evaluate model
│   ├── LICENSE
│   ├── model.py - BERT model
│   ├── requirements.txt
│   └── train.py - main script to invoke all the training and model scripts and save model
├── dags/ - folder with airflow dags
│   ├── annotate_dag.py - annotation pipeline dag
│   ├── inference_dag.py - inference pipeline dag
│   └── training_dag.py - training pipeline dag
├── inference/ folder with inference pipeline to hit dockerised flask API
│   ├── CompanyList.csv - list of company to hit Fast API to get transcripts
│   ├── flask_scraperAPI.py - script to hit simulated scraper - FastAPI  
│   ├── read_flaskAPI.py - hit flask API to get inference of sentences
│   ├── read_scraperAPI.py - read trancript and breakdown to sentences
│   └── save_inference_s3.py - save the csv to s3
├── README.md
└── training_model/ folder with training pipeline scripts
    ├── csv_s3_download.py - save csv to s3
    ├── Labeled.csv 
    └── model_s3_upload.py - upload trained model to S3
```


## Codelab Document:
For more information refer the [document](https://codelabs-preview.appspot.com/?file_id=1Lb87QSg0_9IAE_sXoK1Y7M6gNXkPkwvKuieT0NxWzN8#0)
