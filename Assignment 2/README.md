# Introduction:

  In this assignment, we build a sentiment analysis micro service that could take a new Edgar file in json format and generate sentiments for each
  statement in the referenced EDGAR file and store it on S3 bucket.
 
 As part of the assignment, we orchestrated Airflow Pipelines as mentioned below:
   * Annotation Pipeline: We built pipeline using Airflow for pre processing and labeling the data using AWS comprehend API 
   * Training Pipeline: We configured the pipeline to train a sentiment analysis model using BERT on saved data
   * Inference Pipeline: We designed the inference pipeline to take new data in json format and get back the predictions from the microservice running on the Docker image
     created 
     
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
