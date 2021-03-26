
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from training_model import model_s3_upload, csv_s3_download
from BERT_model import train


def download_from_s3():
    csv_s3_download.download_from_s3('LabeledData/Labeled.csv')

def training_model():
    train.run()

def upload_model_to_s3():
    model_s3_upload.upload_model_to_s3('model.bin')

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('Training-Pipeline',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_download = PythonOperator(task_id='Download-CSV-From-S3',
                              python_callable=download_from_s3)
    t1_train = PythonOperator(task_id='Training-Model',
                                python_callable=training_model)
    t2_upload = PythonOperator(task_id='Upload-Model-To-S3',
                                python_callable=upload_model_to_s3)

t0_download >> t1_train >> t2_upload