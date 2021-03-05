from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from config import config

#connection
engine = create_engine(URL(
    account = config.account,
    user = config.username,
    password = config.password,
    database = config.database,
    schema = config.schema,
    warehouse = config.warehouse,
    role= config.role,
))

print(engine)
connection = engine.connect()

def query(connection,sql):
    try:
        cursor = connection.execute(sql)
        for c in cursor:
            print(c)
        cursor.close()
    finally:
        connection.close()
        engine.dispose()

#SQL Query
sql = 'SELECT * FROM STORM_DETAILS LIMIT 20'
query(connection, sql)