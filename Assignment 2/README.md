# Introduction:

  In this assignment, we build a sentiment analysis micro service that could take a new Edgar file in json format and generate sentiments for each
  statement in the referenced EDGAR file and store it on S3 bucket.
 
 As part of the assignment, we orchestrated Airflow Pipelines as mentioned below:
 
  * Annotation Pipeline: We built pipeline using Airflow for pre processing and labeling the data using AWS comprehend API 
  * Training Pipeline: We configured the pipeline to train a sentiment analysis model using BERT on saved data
  * Inference Pipeline: We designed the inference pipeline to take new data in json format and get back the predictions from the microservice running on the Docker image
     created 
     
 ## Running the Flask Server on Docker Image:
 
 ![MicrosoftTeams-image 9](https://user-images.githubusercontent.com/78016518/112602815-89481b80-8dea-11eb-8e6b-34427700924e.png)
  
  The objective of the project is to POST the input in JSON format to the flask server running on a docker file 
  which returns the sentiment for the input using the pretrained saved model
  
  To serve the provided pre-trained model, follow these steps:
  
   * git clone this repo
   * cd Assignment2/Bert_model
   * Use the ```docker build -t edgar:latest .```  to create docker image which creates a blueprint of the environment with all the requirements
   * Run ```docker images``` & find the image id of the newly built Docker image
   * To run the docker image -- ```docker run -it --rm -p 5000:5000 {image_id}```
     
   If everything worked properly, you should now have a container running, which:
   Spins up a Flask server that accepts POST requests at http://0.0.0.0:5000/predict
   
   To test :
   Write your own POST request (e.g. using [Postman](https://www.postman.com/), here is an example response:
  
  ```
   {
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
            0.19903425872325897     # closer to 0 => negative
        ]
    ]
}
```

    you can also pass a Curl command from the terminal once the Docker image is up and running. Example:
    
    ```
    curl -i -H "Content-Type: application/json" \
		    -X POST -d '{"data": ["this is the best!", "this is the worst!"]}' http://0.0.0.0:5000/predict
    ```
    
    
 ## Annotation Pipeline:
   * Uploading the provided data on s3 bucket 
   * Accessing the data on s3 Preprocessing the data into list of sentences and Using Amazon Comprehend to label the lines with the sentiment analysis score 
   * Scaling the returned output and storing the data on AWS s3 Bucket

 ## Training Pipeline:
   * Built a configurable pipeline to access the data on s3 bucket, train the model and upload the saved model to s3 bucket 
   * Used the BERTBaseUncased model to train and fine tune on labeled data to predict the sentiment of the data
   * Saving the trained model to s3 bucket in .bin format 
    
## inference pipeline:
   * The pipeline would dynamically get the file from EDGAR, pre-process the file,create a list ofsentences for inference. 
   * Jsonify the sentences and invoke the the flask server runnning on the docker image 
   * Post the input data and get back the sentiments and Format the output to a csv file and store it to a bucket.




```
Assignment 2/
├── annotation/
│   ├── csv_s3_upload.py
│   ├── edgar_sentiment_analysis.py
│   ├── s3_upload.py
│   └── scaling.py
├── BERT_model/
│   ├── app.py
│   ├── config.py
│   ├── dataset.py
│   ├── Dockerfile
│   ├── engine.py
│   ├── LICENSE
│   ├── model.py
│   ├── requirements.txt
│   └── train.py
├── dags/
│   ├── annotate_dag.py
│   ├── inference_dag.py
│   └── training_dag.py
├── inference/
│   ├── CompanyList.csv
│   ├── flask_scraperAPI.py
│   ├── read_flaskAPI.py
│   ├── read_scraperAPI.py
│   └── save_inference_s3.py
├── README.md
└── training_model/
    ├── csv_s3_download.py
    ├── Labeled.csv
    └── model_s3_upload.py
```
