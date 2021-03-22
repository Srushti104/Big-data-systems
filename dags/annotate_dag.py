
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import s3_upload
import edgar_sentiment_analysis
import csv_s3_upload

def upload_to_s3():
    s3_upload.upload_to_s3()

def sentiment_analysis():
    edgar_sentiment_analysis.cleaning_files()

def upload_csv_to_s3():
    csv_s3_upload.upload_csv_to_s3()

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('Annotation-Pipeline',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_start = PythonOperator(task_id='UploadFilesToS3',
                              python_callable=upload_to_s3)
    t1_cleanup = PythonOperator(task_id='SentimentAnalysis',
                                python_callable=sentiment_analysis)
    t2_csv = PythonOperator(task_id='UploadCSVToS3',
                                python_callable=upload_csv_to_s3)
    # t3_train = PythonOperator(task_id='TrainModel',
    #                           python_callable=model_training)
    # t4_upload = PythonOperator(task_id='UploadModelsPostTraining',
    #                            python_callable=push_models_to_s3)

t0_start >> t1_cleanup >> t2_csv