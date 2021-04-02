import snowflake.connector as sf
#from config import config
from config import config


# configure connection

def ingest_db():
    conn = sf.connect(user=config.username, password=config.password, account=config.account)

    def query(connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    try:
        sql = 'use {}'.format(config.database)
        query(conn, sql)
        sql = 'use warehouse {}'.format(config.warehouse)
        query(conn, sql)

        try:
            sql = 'alter warehouse {} resume'.format(config.warehouse)
            query(conn, sql)
        except:
            pass

        # SQL query
        csv_file='/Users/akshaybhoge/PycharmProjects/StockAPI/data/datanew.csv'
        sql='put file://{0} @{1}'.format(csv_file, config.stage_table)
        query(conn, sql)
        sql= "copy into {0} from @{1}/datanew.csv FILE_FORMAT=(TYPE=csv skip_header=1)"\
             " ON_ERROR = 'ABORT_STATEMENT' ".format(config.table, config.stage_table)
        query(conn, sql)

    except Exception as e:
        print(e)

    finally:
        conn.close()


ingest_db()