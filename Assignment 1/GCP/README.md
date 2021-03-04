# Google Cloud Platform

In this assignment we are be exploring a sample dataset of SEVIR+NOAA Storm data loaded to Google cloud storage.
We Build a data processing pipeline and ingest the data to bigquery from Google cloud Storage using Apache Beam, DataFlow and explore the sampled data using
Big Query and Data Studio

__Dataflow__ is a managed service for executing a wide variety of data processing patterns. When you run your pipeline with the Cloud Dataflow service, the runner uploads your executable code and dependencies to a Google Cloud Storage bucket and creates a Cloud Dataflow job, which executes your pipeline on managed resources in Google Cloud Platform.[1](https://medium.com/google-cloud/basic-streaming-data-enrichment-on-google-cloud-with-dataflow-sql-a7684353119c)

__Datalab__ is used to explore, analyze, transform data and build Machine Learning (ML) models on Google’s Cloud virtual machine. 

__BigQuery__ is cloud-based big data analytics web service for processing very large read-only data sets, using SQL-like syntax

__DataStudio__ Data Studio is a free tool that turns your data into informative, easy to read, easy to share, and fully customizable dashboards and reports.

## Architecture:
![image](https://user-images.githubusercontent.com/78016518/110038226-73749880-7d0d-11eb-80aa-b44c75b67d2a.png)


## Configuration:
  * Create a GCP account using the link https://console.cloud.google.com/getting-started
  * Enable the following API’s: BigQuery API, AI Platform, Cloud Source Repositories, Dataflow, Data Labeling,Big Query, Data Studio on GCP
  * Create a datalab instance on GCP
  * Python 3 
  
## Requirments:

### Upload sample data to Cloud Storage
   * Create a Storage Bucket on GCP
   * Create an IAM role and a download a Secret Access Key JSON file from GCP which should be used to connect to Google Cloud Storage bucket 
   * Provide the JSON file path and the bucket name in py file
   * Install the dependencies on the local machine
  ```  
      --pip install google-cloud-storage
   ``` 
   
 ### Launching Datalab:
    
   * Create a New Project on GCP 
   * Connect to google Cloud Shell
   * Run command to enter into the project created from the cloud shell
  ```
      --gcloud config set project Project-ID
  ``` 
   * Create a Datalab instance
  ```  
      --datalab create --zone us-central1-a mydatalab
   ``` 
   
### Pipeline for Processing and loading the Data to Big query
   
   * Install the following dependencies prior to running the notebook
``` 
   pip install --ignore-installed --upgrade pytz==2018.4
   pip uninstall -y google-cloud-dataflow
   pip install --upgrade apache-beam[gcp]==2.12.0
   pip install google-cloud-bigquery --upgrade
```

  * Once done import the foloowing packages
```
   import apache_beam as beam
   import argparse
   from apache_beam.options.pipeline_options import PipelineOptions
   from sys import argv
```
  * Change the project_ID variable  
 





