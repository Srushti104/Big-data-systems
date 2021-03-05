# Snowflake



## Setup

**snowflake**
Create free trail snowflake account.
Login to the account using the url you receive in mail.

**Apache Superset** is a modern, enterprise-ready business intelligence web application. It is fast, lightweight, intuitive, and loaded with options that make it easy for users of all skill sets to explore and visualize their data, from simple pie charts to highly detailed deck.gl geospatial charts.

**apache superset**
Install xcode.  

```xcode-select --install``` 

Make sure you have latest version of pip and setup tools. 

```pip install --upgrade setuptools pip```

Setup Virtual Environment, you can also create Pycharm project and have separate environment.   
  
Install apache-suprset.  

```pip install apache-superset```

Initialize Database.  

```superset db upgrade```

Create an admin user (you will be prompted to set a username, first and last name before setting a password).   

```export FLASK_APP=superset```
```superset fab create-admin```

Load some data to play with.   

```superset load_examples```

Create default roles and permissions.   
```superset init```

To start a development web server on port 8088, use -p to bind to another port.


```superset run -p 8088 --with-threads --reload --debugger```.   

You will get local host link at port 8088. Navigate to hostname:port and Login to link with user and password you have set in previous step.  

  
## Configuration. 
 
Create DB using the script.   
<script name>.    
  
  
  
Load DB from S3 using below command:     
<script name>.    
  

The recommended connector library for Snowflake is snowflake-sqlalchemy.    
Install python libarary before running the script.    
```pip install snowflake-sqlalchemy```.   

  
Query the table using python script.    
<script name>.     
      

## Connecting to superset.   

got to Dataset option. Connection. 


```snowflake://{user}:{password}@{account}.{region}/{database}?role={role}&warehouse={warehouse}```    


Once all the data is fecthed you can analyse the data by creating charts and dashboards.
