from predict import get_score

try:
    import io
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union
    import cv2
    import numpy as np
    import pandas as pd
    import streamlit as st
    # from predict import get_score
except Exception as e:
    print(e)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""


class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["png", "jpg"]

    def option(self):
        print('Hello')

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.title('Acne Classifier')
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", ["Home", "Built-In Examples", "Upload your custom Image"])

        if selection == "Home":
            st.markdown(
                '''
                ## Acne Type Classification Pipeline using CNN 

        The training pipeline aims to identify the type of Acne-Rosacea, by training a model with images scraped from dermnet.com with a confidence score.
        The front-end application uses Streamlit to predict using the trained model.
        
        
        #### Model - MobileNet (CNN) 
        - Depthwise Separable Convolution is used to reduce the model size and complexity. It is particularly useful for mobile and embedded vision applications
        - The model can be used in edge devices such as IoT devices or mobile applications - owing to its small size.
        
        #### Continuous Model Integration
        
        - Made possible by chaining all processes using Airflow
        - The pipeline can be scheduled to run at a predefined cadence and is constantly retraining the model
        - Continuously upload the trained graph and labels to S3
        
        
        ### Training Pipeline
        
        Airflow is a platform to programmatically author, schedule and monitor workflows.
        Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. 
        
        The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. [1]
        
        #### Use Cases
        
        - Replace cron jobs: Monitoring cron jobs is hard and tedious. Instead of manually ssh to servers to find out if/why your jobs fail, you can visually see whether your code run or not through the UI and have Airflow notifies you when a job fails.
        - Extract data: Airflow, with its many integrations, are used a lot for data engineering tasks. You can write tasks to extract data from your production databases, check data quality, and write the results to your on-cloud data warehouse.
        - Transform data: You can interface with external services to process your data. For example, you can have a pipeline that submits a job to EMR to process data in S3 with Spark and writes the results to your Redshift data warehouse.
        - Train machine learning models: You can extract data from a data warehouse, do feature engineering, train a model, and write the results to a NoSQL database to be consumed by other applications.
        - Crawl data from the Internet: You can write tasks to periodically crawl data from the Internet and write to your database. For instance, you can get daily competitor’s prices or get all comments from your company’s Facebook page. [2]
        
        ### Requirements
        
        Install the dependencies as outlined in the `requirements.txt` by running
        ```
        pip install -r requirements.txt
        ```
        
        ### Getting Started 
        
        ```
        airflow_cnn_pipeline/
        ├── app.py
        ├── dags/
        │   ├── retrain.py
        │   └── train_model.py
        ├── models/
        │   ├── Mobilenet/
        │   │   └── mobilenet_v1_1.0_224/
        │   │       ├── frozen_graph.pb
        │   │       ├── labels.txt
        │   │       └── quantized_graph.pb
        │   ├── retrained_graph_v2.pb
        │   └── retrained_labels.txt
        ├── predict.py
        ├── requirements.txt
        ├── s3_uploader/
        │   ├── __init__.py
        │   └── upload_models.py
        ├── scraper/
        │   ├── __init__.py
        │   └── dermnet_scrape.py
        └── train.py
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
        
        ### Inference
        
        The Streamlit app can be used for Inference. Start the server by running `streamlit run app.py` from your terminal. Open the app by visiting http://localhost:8501 on your browser.
        
        Alternatively, you may use the `predict.py` script for inference. Provide the path to your image and run the script.
        
        
        #### Citation & References
        
        [[1] Apache Airflow](https://airflow.apache.org/) <br/>
        [[2] Tuan Nguyen](https://towardsdatascience.com/getting-started-with-airflow-locally-and-remotely-d068df7fcb4) <br/>
        [Hands-On Deep Learning for IoT](https://www.packtpub.com/product/hands-on-deep-learning-for-iot/9781789616132) <br/>
        [GitHub: PacktPublishing/Hands-On-Deep-Learning-for-IoT](https://github.com/PacktPublishing/Hands-On-Deep-Learning-for-IoT) <br/>
                        
                        
                
                '''
            )

        if selection == "Built-In Examples":
            st.subheader("Use Built-In examples")
            st.image('./demo_img/test1.jpg', width=200)
            if st.button('Example 1'):
                df = get_score('./demo_img/test1.jpg')
                df2 = df.set_index('Issue')
                st.dataframe(df)
                st.bar_chart(df2)
            st.image('./demo_img/test2.jpg', width=200)
            if st.button('Example 2'):
                df = get_score('./demo_img/test2.jpg')
                df2 = df.set_index('Issue')
                st.dataframe(df)
                st.bar_chart(df2)

            st.image('./demo_img/test3.jpg', width=200)
            if st.button('Example 3'):
                df = get_score('./demo_img/test3.jpg')
                df2 = df.set_index('Issue')
                st.dataframe(df)
                st.bar_chart(df2)

            st.image('./demo_img/test4.jpg', width=200)
            if st.button('Example 4'):
                df = get_score('./demo_img/test4.jpg')
                df2 = df.set_index('Issue')
                st.dataframe(df)
                st.bar_chart(df2)
        elif selection == "Upload your custom Image":

            st.markdown(STYLE, unsafe_allow_html=True)
            file = st.file_uploader("Upload file", type=self.fileTypes)
            show_file = st.empty()
            if not file:
                show_file.info("Please upload a file of type: " + ", ".join(["png", "jpg"]))
                return

            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)
            cv2.imwrite('out.jpg', opencv_image)
            df = get_score('out.jpg')

            df2 = df.set_index('Issue')
            st.dataframe(df)
            st.bar_chart(df2)

            if isinstance(file, BytesIO):
                show_file.image(file)
            else:
                data = pd.read_csv(file)
                st.dataframe(data.head(10))
            file.close()


if __name__ == "__main__":
    helper = FileUpload()
    helper.run()
