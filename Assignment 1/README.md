# Assignment 1

In this assignement we work on devoloping data pipeline to ingest, process, store Sevir and Storm Data.Access it through 3 different Architectures and understand the differences 
between these Architectures. And discuss on the challenges faced in each architecture.

  * AWS
  * GCP 
  * SnowFlake

Below are the links for the datasets

  * [Storm DataSet](https://www.ncdc.noaa.gov/stormevents/ftp.jsp "Storm Dataset")

  * [Storm DataSet Metadata](https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Export-Format.pdf)

  * [SEVIR Tutorial Notebook](https://nbviewer.jupyter.org/github/MIT-AI-Accelerator/eie-sevir/blob/master/examples/SEVIR_Tutorial.ipynb). 

  * [SEVIR S3 Bucket](https://s3.console.aws.amazon.com/s3/buckets/sevir?prefix=data/&showversions=false). 

 ## AWS Architecture:
 
   * Upload a sample of Sevir and Storm data to Amazon S3 storage bucket 
   * Experimenting with Amazon Glue and build a pipeline.
   * Using Amazon Quicksight to query and build visulizations
 
 ## GCP Architecture:
  
   * Download sample datasets and move it to Google storage buckets
   * Experiment with Google Dataflow and build a pipeline to process the data and ingest the data to Big query
   * Show how Google Bigquery and Data studio to query and build visulizations

 ## SnowFlake Architecture:
   
   * Moving the sample data to snowflake 
   * Using Sql Alchemy and ApacheSuperset to query and build visulizations 

For more detailed information please refer to the folders associated to the Architecture

 ## Codelab Document:
 Please refer the [document](https://codelabs-preview.appspot.com/?file_id=1WaIYSb5BqgXXUkx8QnvYN9F2jepINcSv0UbK-06tcps#0) 
