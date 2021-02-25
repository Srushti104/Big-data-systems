# Lab 5 - Snowflake


Snowflake is a cloud Data warehouse offered as Software-as-a-Service(SaaS) on multiple clouds(AWS and Azure) for analytics workload. This is a cloud service similar to AWS Redshift.

There are 3 major components:
* Cloud services: This component takes care of a variety of services like Authentication, Access control, Metadata management, Infrastructure management, Query Parsing, and optimization.
* Query processing: Snowflake has a concept of virtual warehouses which are like a separate MPP cluster which can be instantiated on demand. They come in different sizes X-small to 4X-Large and snowflake charges based on the size of the virtual warehouse. Each virtual warehouse is an independent entity and does not share any compute resources with other virtual warehouses and the performance of 1 virtual warehouse is not affected by others.
* Database storage: Data stored in snowflake is automatically optimized, compressed into a proprietary columnar format and this is stored in Cloud storage like S3 or Azure blob storage. Snowflake manages how it is stored, where it is stored and is only accessible by SQL queries run using snowflake.[[1](https://medium.com/@achilleus/snowflake-cloud-data-warehouse-66569157a399)]



## Lab completion date - 02/17/2021

## Setup:

- Snowflake account - Standard (Free trial account)
- Choose Cloud Provider - AWS
- Set Region - US East

## Hands on
* Creating Databse
* Loading database from S3
* Replication Databse based on use case
* Creating user roles
* Resetting environment

Link to [Webinar Zero to Snowflake in 90 minutes](https://guides.snowflake.com/guide/getting_started_with_snowflake/#0)

## CodeLab document:  
https://codelabs-preview.appspot.com/?file_id=1UVHcXn-L02bQKkmgh6N_Lyg0SC4suv8IdJCXBEoW_F0#0


