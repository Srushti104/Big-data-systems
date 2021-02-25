# Lab 2 - GCP- DataFlow,Datalab

In this lab, we will explore a structured dataset and then create training and evaluation datasets using Dataflow for a machine learning (ML) model.

__Dataflow__ is a managed service for executing a wide variety of data processing patterns. When you run your pipeline with the Cloud Dataflow service, the runner uploads your executable code and dependencies to a Google Cloud Storage bucket and creates a Cloud Dataflow job, which executes your pipeline on managed resources in Google Cloud Platform.[1](https://medium.com/google-cloud/basic-streaming-data-enrichment-on-google-cloud-with-dataflow-sql-a7684353119c)

__Datalab__ is used to explore, analyze, transform data and build Machine Learning (ML) models on Google’s Cloud virtual machine. 

__BigQuery__ is cloud-based big data analytics web service for processing very large read-only data sets, using SQL-like syntax.

## Lab completion date - 


## Setup:

   * Create a GCP account
   * Create a new project -babyweight-project
   * Enable the following API’s: BigQuery API, AI Platform, Cloud Source Repositories, Dataflow, Data Labeling
   * Create a datalab instance 
   * Python 3 
   * Tensor flow 
   * Apache beam


## Configuration:

### Launching Datalab:

   * Run command --gcloud config set project babyweight-project-- to enter into the project created from the cloud shell 
   * Create a Datalab instance using --gcloud config set project (babyweight-project)
   * Make sure the project name is same the projectId created on GCP
   * Once the instance has been created change the port to 8081
 
### Clone datalab notebook:

   * Create a new notebook and then run the following command to clone the repo--!git clone https\://github.com/GoogleCloudPlatform/training-data-analyst
   * In Datalab, open the notebook --training-data-analyst/blogs/babyweight/babyweight.ipynb.

## CodeLab document:

https://codelabs-preview.appspot.com/?file_id=1U5hDAUHTgloic_77oFvMeox299I9D2zWlN0fZhhgvIo#0
 

