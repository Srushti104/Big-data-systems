from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import ingest_db,merge_files


def merge_files1():
    merge_files.merge()

def ingest_db1():
    ingest_db.ingest_db()


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('Ingestion-Pipeline',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_start = PythonOperator(task_id='Merge-files',
                              python_callable=merge_files1)
    t1_cleanup = PythonOperator(task_id='Ingest-snowflake-db',
                                python_callable=ingest_db1)

t0_start >> t1_cleanup