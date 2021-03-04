# Amazon Web Service (AWS)

[SEVIR Tutorial Notebook](https://nbviewer.jupyter.org/github/MIT-AI-Accelerator/eie-sevir/blob/master/examples/SEVIR_Tutorial.ipynb). 

[SEVIR S3 Bucket](https://s3.console.aws.amazon.com/s3/buckets/sevir?prefix=data/&showversions=false). 

## Setup 
Signup for an AWS Account [here](https://console.aws.amazon.com/console/home?region=us-east-1#)  
The pipeline requires below Amazon Web Services to deploy and run.

- Two S3 to store files
- Two Lambda 
- Two CloudWatch one rule on the AWS Glue crawler and another on the AWS Glue ETL job.
- Glue to perform ETL
- Athena to query the data
- Quicksight to analyse and created dashboards
- Identity and Access Management (IAM) roles for accessing AWS Glue, Amazon SNS, Amazon SQS, and Amazon S3.

The script samples the data for 2019-01 to copy files from SEVIR S3 bucket to your bucket.
> ```copys3_to_s3.py``` 

Script to upload file to S3
> ```s3_upload```

## Data Pipeline

Ingested data lands in an Amazon S3 bucket we named it as sevirdatapipeline-raws3bucket.  
To make that data available, we have to catalog its schema in the AWS Glue Data Catalog.  
We did this using an AWS Lambda function invoked by an Amazon S3 trigger to start an AWS Glue crawler that catalogs the data. 
When the crawler is finished creating the table definition, we invoke a second Lambda function using an Amazon CloudWatch Events rule. This step starts an AWS Glue ETL job to process and output the data into another Amazon S3 bucket sevirdatapipeline-processeds3bucket.  Once the processed data reaches S3 we pick the output S3 from quicksight to crate Dashboard.

## Architecture



* Python script to read HDF5 file.
> ```h5_read_file.py```. 
* Python script to read and sample data in HDF5 file based on year and month. 
> ```read_h5.py```. 






