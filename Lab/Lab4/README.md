# Lab 4 - SQL Alchemy

SQLAlchemy provides a nice “Pythonic” way of interacting with databases. So rather than dealing with the differences between specific dialects of traditional SQL such as MySQL or PostgreSQL or Oracle, you can leverage the Pythonic framework of SQLAlchemy to streamline your workflow and more efficiently query your data. 


## Lab completion date - 02/12/2021

## Setup:

- Setup Project in Pycharm with virtual environment
- Install Python Packages
```
$ pip install sqlalchemy 
$ pip install psycopg2-binary 
```
In base.py script set up Postgres connection url as per you port 
```
postgresql://localhost:1800/postgres
```

## Configuration:
Setup base.py script to connect to Postgres DB

Connecting to Database:
```
import sqlalchemy as db
engine = db.create_engine('dialect+driver://user:pass@host:port/db')
```

## CodeLab document:  
https://codelabs-preview.appspot.com/?file_id=1W2rSmS3Xvj2T2jowlxd-dWCOLhdimBsIhjftX0pfxu8#0


