# Imports the modules
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Import Custom Modules
from s3_uploader import upload_models
from scraper import dermnet_scrape


def push_models_to_s3():
    upload_models.upload_to_s3()


def scrape_from_dermnet():
    # Get all data from Dermnet
    dermnet_scrape.get_data()


def clean_data():
    import os
    import shutil
    folders = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ScrapedData-Acne-and-Rosacea-Photos'))

    for folder in list(os.walk(folders)):
        if not os.listdir(folder[0]):
            os.removedirs(folder[0])

    for folder in list(os.walk(folders)):
        if len(os.listdir(folder[0])) < 15:
            print(folder[0] + ' removed')
            shutil.rmtree(folder[0])


def model_training():
    from subprocess import call
    call(["python", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'train.py'))])


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('CNN-Training-Pipeline',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_start = PythonOperator(task_id='UploadModels',
                              python_callable=push_models_to_s3)
    t1_getdata = PythonOperator(task_id='ScrapeData',
                                python_callable=scrape_from_dermnet)
    t2_cleanup = PythonOperator(task_id='Cleanup',
                                python_callable=clean_data)
    t3_train = PythonOperator(task_id='TrainModel',
                              python_callable=model_training)
    t4_upload = PythonOperator(task_id='UploadModelsPostTraining',
                               python_callable=push_models_to_s3)

t0_start >> t1_getdata >> t2_cleanup >> t3_train >> t4_upload
