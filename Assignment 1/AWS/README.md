# Amazon Web Service (AWS)

**Amazon Simple Storage Service (Amazon S3)** is an object storage service that offers industry-leading scalability, data availability, security, and performance.

**AWS Glue** is a serverless data integration service that makes it easy to discover, prepare, and combine data for analytics, machine learning, and application development.   


A **crawler** can crawl multiple data stores in a single run. Upon completion, the crawler creates or updates one or more tables in your **Data Catalog**. Extract, transform, and load (ETL) jobs that you define in AWS Glue use these Data Catalog tables as sources and targets. The ETL job reads from and writes to the data stores that are specified in the source and target Data Catalog tables.  


**AWS Lambda** is a serverless compute service that lets you run code without provisioning or managing servers, creating workload-aware cluster scaling logic, maintaining event integrations, or managing runtimes.

**Amazon CloudWatch** is a monitoring and observability service built for DevOps engineers, developers, site reliability engineers (SREs), and IT managers.

## Setup 
Signup for an AWS Account [here](https://console.aws.amazon.com/console/home?region=us-east-1#)  
The pipeline requires below Amazon Web Services to deploy and run.

- Two S3 to store files
- Two Lambda 
- Two CloudWatch one rule on the AWS Glue crawler and another on the AWS Glue ETL job.
- Glue to perform ETL
- Athena to query the data
- Quicksight to analyse and created dashboards
- Identity and Access Management (IAM) roles for accessing AWS Glue, Amazon SNS, and Amazon S3.

The script samples the data for 2019-01 to copy files from SEVIR S3 bucket to your bucket.
> ```copys3_to_s3.py``` 

Script to upload file to S3
> ```s3_upload```

## Configuration
* Create IAM roles - AWS Glue, Amazon SNS,  and Amazon S3.
* Create Lambda function 
* Configure an Amazon S3 bucket event trigger. 
    when new data lands in the bucket, you trigger GlueTriggerLambda using Event notification
* Automate the Data Catalog with an AWS Glue crawler. 
  After you upload the data into the raw zone, the Amazon S3 trigger that you created earlier in the post invokes the GlueTriggerLambdafunction. This function creates an AWS Glue Data Catalog that stores metadata information inferred from the data that was crawled.  
* Connect ETL jobs with AWS Glue. 
  Create Job in AWS GLue and select IAM role. Choose the target format of file as CSV and save the job.
* Automate ETL job execution
  In Lambda function configure your ETL job name and the CloudWatch Events rule. 

## Data Pipeline

1. Ingested data lands in an Amazon S3 bucket we named it as sevirdatapipeline-raws3bucket. 
2. To make that data available, we have to catalog its schema in the AWS Glue Data Catalog.  
3. We did this using an AWS Lambda function invoked by an Amazon S3 trigger to start an AWS Glue crawler that catalogs the data. 
4. When the crawler is finished creating the table definition, we invoke a second Lambda function using an Amazon CloudWatch Events rule. 
5. This step starts an AWS Glue ETL job to process and output the data into another Amazon S3 bucket sevirdatapipeline-processeds3bucket.  
6. Once the processed data reaches S3 we pick the output S3 from quicksight to crate Dashboard.

## Architecture
![SEVIR_AWS](https://user-images.githubusercontent.com/59776740/110042602-057f9f80-7d14-11eb-845c-2e020d9db1ed.png)



* Python script to read HDF5 file.
> ```h5_read_file.py```. 
* Python script to read and sample data in HDF5 file based on year and month. 
> ```read_h5.py```. 
From above script we can find the list of filename and index. With these details we can run the script
> ```save_g5_img.py```






