# Airflow_TFX

From https://www.tensorflow.org/tfx/tutorials/tfx/airflow_workshop
Codebase available here: https://github.com/tensorflow/tfx/tree/master/tfx/examples/airflow_workshop

## Introduction:

  Apache Airflow is an open-source platform to Author, Schedule and Monitor workflows. Airflow helps you to create workflows using Python programming language and these workflows   can be scheduled and monitored easily with it.

## Configuration:
   
   * install all the requirmensts 
   
   ```
   pip install -r rwquirments.txt
   
   ```
   * Airflow setup
   ```
   export AIRFLOW_HOME=<pwd>
   ```
   * Initalise DB
   ```
   airflow db init
   ```
   * airflow users create \ --username admin \ --firstname <YourName> \ --lastname <YourLastName> \ --role Admin \ --email example@example.com -create user
   * Start Airflow in deamon mode 
   ```
  airflow webserver -D
  ```
  * Start airflow Schedular 
  ```
  airflow scheduler
  ```
  
  * Once both are running - you should be able to access the Airflow UI by visiting http://127.0.0.1:8080/home on your browser.
  * To kill the Airflow webserver daemon:
  ```
  lsof -i tcp:8080  
  ```
  
  * Kill the process by running kill <PID> - in this case, it would be kill 13280
  



