
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from inference import read_flaskAPI, read_scraperAPI,save_inference_s3


# def read_scraper_API():
#     read_scraperAPI.read_scraper_API()
#
# def scraped_csv():
#     sentence = read_flaskAPI.read_scraped_csv('/Users/akshaybhoge/PycharmProjects/Edgar/inference/Inference-transcript.csv')
#     return sentence
#
# def read_inference_API():
#     #sentence = read_scraped_csv()
#     scraped_csv
#     response = read_flaskAPI.read_inference_API(sentence)
#     return response
#
# def json_to_csv():
#
#     read_flaskAPI.json_to_csv(response)

def read_scraper_API():
     read_scraperAPI.read_scraper_API()

def read_scraped_csv():
    sentence = read_flaskAPI.read_scraped_csv('/Users/akshaybhoge/PycharmProjects/Edgar/inference/Inference-transcript.csv')
    response = read_flaskAPI.read_inference_API(sentence)
    read_flaskAPI.json_to_csv(response)

def upload_inference_to_s3():
    save_inference_s3.upload_inference_to_s3('Inference-Labeled')

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('Inference-Pipeline',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_download = PythonOperator(task_id='Read-Scraper-API',
                              python_callable=read_scraper_API)
    t1_train = PythonOperator(task_id='Get-Inference-API',
                                python_callable=read_scraped_csv)
    t2_upload = PythonOperator(task_id='Save-Inference-CSV-to-S3',
                                python_callable=upload_inference_to_s3)


t0_download >> t1_train >> t2_upload