import inspect
import os
import sys

from fastapi import FastAPI

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from get_image import download
from predict import get_score

app = FastAPI()


@app.get("/predict/{img_url:path}")
def get_inference(img_url: str):
    # Get the image file from the URL
    local_path = download.fetch(img_url)

    # Get predicted values
    df = get_score(os.path.join(os.path.dirname(__file__), local_path))
    a = df.to_dict()

    # Return the issue & confidence
    return a


@app.post("/pipeline/start")
def start_pipeline():
    run_details = os.system('airflow dags trigger CNN-Training-Pipeline')
    # Return the issue & confidence
    return {"status": "Airflow Pipeline Started", "details": run_details}


@app.post("/pipeline/config")
def start_server():
    os.system('airflow webserver -D')
    os.system('airflow scheduler')
    # Return the issue & confidence
    return {"Airflow Webserver & Scheduler Started"}
