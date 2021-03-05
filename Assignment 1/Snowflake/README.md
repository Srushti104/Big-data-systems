
# Snowflake   

**Snowflake** is a cloud data warehouse built on top of the Amazon Web Services (AWS) cloud infrastructure and is a true SaaS offering. There is no hardware (virtual or physical) for you to select, install, configure, or manage. There is no software for you to install, configure, or manage. All ongoing maintenance, management, and tuning is handled by Snowflake.   

**Apache Superset** is a modern, enterprise-ready business intelligence web application. It is fast, lightweight, intuitive, and loaded with options that make it easy for users of all skill sets to explore and visualize their data, from simple pie charts to highly detailed deck.gl geospatial charts.[Link](https://superset.apache.org/)


## Setup

**Snowflake**
Create free trail snowflake account. [Here](https://signup.snowflake.com/?_bt=470247374333&_bk=snowflake&_bm=e&_bn=g&_bg=64805047909&utm_medium=search&utm_source=adwords&utm_campaign=NA%20-%20Branded%20-%20Exact&utm_adgroup=NA%20-%20Branded%20-%20Snowflake%20-%20Exact%20RSA&utm_term=snowflake&utm_region=na&gclid=CjwKCAiAp4KCBhB6EiwAxRxbpNlQPIY3MoontJCloX6Xt5Zcjwu6eDUdAdkRVqa4JhbGNqBRG7Hb6RoCm-8QAvD_BwE). 
Login to the account using the url you receive in mail.

**Apache Superset** 

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
```create_<filename>_DB.sql```     
  
  
Load DB from S3 using below command:       
```load_<filename>_DB.sql```      
    

The recommended connector library for Snowflake is snowflake-sqlalchemy.     
Install python libarary before running the script.     
```pip install snowflake-sqlalchemy```       
 
  
Query the table using python script. 
 
> NOTE : Update the ```config.py``` file before running the script with your account details.  

```snowflake_sqlalchemy.py```   

```queries.sql```          
      

## Connecting to superset.   

Navigate to Data --> Datasets option. Add Database connection enter the below url    


```snowflake://{user}:{password}@{account}.{region}/{database}?role={role}&warehouse={warehouse}```    


Select your Database, Schema, and Table using the drop downs that appear. Once all the data is fetched you can analyse the data by creating charts and dashboards.
