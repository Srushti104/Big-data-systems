# Lab 1 - AWS Getting Started + Lambda

Amazon S3 service is used for file storage, where you can upload or remove files. We can trigger AWS Lambda on S3 when there are any file uploads in S3 buckets. AWS Lambda has a handler function which acts as a start point for AWS Lambda function. The handler has the details of the events.

AWS Lambda is a service which computes the code without any server. It is said to be serverless compute. The code is executed based on the response of events in AWS services such as adding/removing files in S3 bucket.[1](https://www.tutorialspoint.com/aws_lambda/index.htm)


## Lab completion date - 01/05/2021

## Setup:

-Create AWS account.   
-Setup AWS Command Line Interface.   

AWS Console   
* Create S3 Bucket. 
* Create role which has permission to work with s3 and lambda. 
* Create lambda function and add s3 as the trigger.  


## Configuration:

configure aws account from CLI
```
$ aws configure
AWS Access Key ID [None]: *******************PLE
AWS Secret Access Key [None]: **************************KEY
Default region name [None]: 
Default output format [None]: json
```
Install Faker and boto3 library
```
$ pip3 install Faker
$ pip3 install boto3
```


## CodeLab document:  



