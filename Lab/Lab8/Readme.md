## Lab 8 - Airflow

**Airflow**
Airflow is a workflow management platform developed and open-source by AirBnB in 2014 to help the company manage its complicated workflows.

Airflow was developed with four principles in mind, which are scalable, dynamic, extendable, and elegant. Scalable means you can effortlessly scale your pipeline horizontally. Dynamic means dynamic pipeline generation, extensible means you can easily write your custom operators/integrations. Finally, elegant means you can have your pipeline lean and explicit with parameters and Jinja templating.

In this lab we are building Acne Type Classification Pipeline using CNN 

The training pipeline aims to identify the type of Acne-Rosacea, by training a model with images scraped from dermnet.com with a confidence score.
The front-end application uses Streamlit to predict using the trained model.



#### Model - MobileNet (CNN) 
- Depthwise Separable Convolution is used to reduce the model size and complexity. It is particularly useful for mobile and embedded vision applications
- The model can be used in edge devices such as IoT devices or mobile applications - owing to its small size.

#### Continuous Model Integration

- Made possible by chaining all processes using Airflow
- The pipeline can be scheduled to run at a predefined cadence and is constantly retraining the model
- Continuously upload the trained graph and labels to S3

![pipeline](/airflow_cnn_pipeline/img/airflow.jpg)

### Training Pipeline

Airflow is a platform to programmatically author, schedule and monitor workflows.
Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. 

The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. [1]


### Requirements

Install the dependencies by running `requirements.txt` 
```
pip install -r requirements.txt
```

#### Update S3 Bucket details

Provide the S3 bucket name in the `bucket_name` parameter in `s3_uploader/upload_models.py`

#### Airflow Configuration

Once Airflow is installed, configure the same by running:

```
# Use your present working directory as
# the airflow home
export AIRFLOW_HOME=~(pwd)

# export Python Path to allow use
# of custom modules by Airflow
export PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"


# initialize the database
airflow db init

airflow users create \
    --username admin \
    --firstname <YourName> \
    --lastname <YourLastName> \
    --role Admin \
    --email example@example.com
```

#### Using Airflow

Start the Airflow server in daemon
```
airflow webserver -D
```
Start the Airflow Scheduler
```
airflow scheduler
```

Once both are running - you should be able to access the Airflow UI by visiting http://127.0.0.1:8080/home on your browser.

To kill the Airflow webserver daemon:
```
lsof -i tcp:8080  
```
You should see a list of all processes that looks like this:
```
COMMAND   PID        USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  13280 dileepholla    6u  IPv4 0x8f7b5be5240cda23      0t0  TCP *:http-alt (LISTEN)
Python  13325 dileepholla    6u  IPv4 0x8f7b5be5240cda23      0t0  TCP *:http-alt (LISTEN)
Python  13362 dileepholla    6u  IPv4 0x8f7b5be5240cda23      0t0  TCP *:http-alt (LISTEN)
Python  13401 dileepholla    6u  IPv4 0x8f7b5be5240cda23      0t0  TCP *:http-alt (LISTEN)
Python  13431 dileepholla    6u  IPv4 0x8f7b5be5240cda23      0t0  TCP *:http-alt (LISTEN)
```

Kill the process by running `kill <PID>` - in this case, it would be `kill 13280`

### Running the Pipeline

Login to Airflow on your browser and turn on the `CNN-Training-Pipeline` DAG from the UI. Start the pipeline by choosing the DAG and clicking on Run.


### API Usage

The API endpoints allow the following:
- Starting the Airflow Webserver & Scheduler
- Starting the training pipeline
- Inference

Start the API server by running
```
cd api
uvicorn main:app --reload
```

API Documentation can be viewed by visiting 127.0.0.1:8000/docs

### Inference

#### Using the Streamlit App

The Streamlit app can be used for Inference. Start the server by running `streamlit run app.py` from your terminal. Open the app by visiting http://localhost:8501 on your browser.

#### Using the API Endpoint

Visit 127.0.0.1:8000/docs to view API documentation.

#### Using the Standalone `.py` script

You may use the `predict.py` script for inference. Provide the path to your image and run the script.

#### References

[Apache Airflow](https://airflow.apache.org/)   
[Tuan Nguyen](https://towardsdatascience.com/getting-started-with-airflow-locally-and-remotely-d068df7fcb4)   


[Code Lab Link](https://codelabs-preview.appspot.com/?file_id=1CtkDbPBoAPG0bsOQuIq2d5i6UIiNXjIyKC4vkLh2gvc#0)
