import traceback
from typing import Set, Any

import psycopg2


# setting connection globally
pgconn:psycopg2._psycopg.connection = None
pgcursor:psycopg2._psycopg.cursor   = None
connection_attempts:int = 0
MAX_ATTEMPTS:int = 3

class CustomDbAttemptException(Exception):
    pass

def reconnect():
    global pgconn
    global connection_attempts
    try:
        connection_attempts+=1
        if connection_attempts > MAX_ATTEMPTS:
            raise CustomDbAttemptException("Connection Attempts Expired")
        if pgconn == None or pgconn.closed == True:
            pgconn = psycopg2.connect(host="localhost", port=25432, dbname="postgres", user="postgres", password='Pass2022#')
            connection_attempts = 0
        return pgconn
    except Exception as e:
        print("Reconnecting Attempt :: ",connection_attempts)
        e.with_traceback()
        if isinstance(e,CustomDbAttemptException):
            print("DB Attempt Error: ",e.args)
            raise e
        reconnect()
    finally:
        pass

def getCursor()->psycopg2._psycopg.cursor:
    global pgcursor
    try:
        if pgconn == None or pgconn.closed == True:
            reconnect()
        if pgcursor == None or pgconn.closed == True:
            pgcursor = pgconn.cursor()
        return pgcursor
    except Exception as e:
        e.with_traceback()
        if isinstance(e, CustomDbAttemptException):
            raise e
    finally:
        pass

def check_connection():
    try:
        c=getCursor()

        if pgconn is not None:
            print("cc:: Connection metadata :: ", repr(pgconn.get_dsn_parameters()))
            c.execute("select 1,2,3,4")
            print("cc::Query    :: ", c.query)
            print("cc::Count    :: ", c.rowcount)
            print("cc::Data(0)  :: ", c.fetchone())
            print("cc::Data     :: ", c.fetchall())
            print("Database connected successfully")
        else:
            print("Database is not connected")
    except Exception as e:
        print("Error while connecting Database")
        traceback.print_exc()



def check_again():
    try:
        c=getCursor()
        c.execute("select 22,23,24,25,26")
        print("ca::Query    :: ", c.query)
        print("ca::Count    :: ", c.rowcount)
        print("ca::Data(0)  :: ", c.fetchone())
        print("ca::Data     :: ", c.fetchall())
        print("Database connected successfully")
    except Exception as e:
        traceback.print_exc()

def create_ddl_table():
    c = getCursor()
    c.execute(
        "create table if not exists t_classroom \
        (\
         cid serial primary key,\
         cname varchar (50) unique not null,\
         csection varchar (50) default 'A'\
        );"
    )
    c.connection.commit()

def check_table_entries():
    try:
        c = getCursor()
        c.execute("select * from t_classroom")
        print("ca::Query    :: ", c.query)
        print("ca::Count    :: ", c.rowcount)
        print("ca::Data(0)  :: ", c.fetchone())
        print("ca::Data     :: ", c.fetchall())
        print("Table created successfully")
    except Exception as e:
        traceback.print_exc()

def insert_values (tableName:str, columnNames, columnValues):
    '''
    check the following documentation for passing parameters:
    https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
    :param tableName:
    :param columnNames:
    :param columnValues:
    :return:
    '''
    try:
        c = getCursor()
        # sample
        # "INSERT INTO t_classroom (cname,csection) VALUES (%(cname)s,%(csection)s)",{'cname':'LKG','csection':'A'}
        # format arg1 -> tableName
        # format arg2 -> columnNames -> (col1, col2)
        # format arg3 -> positionalParam -> (%(key1)s,%(key2)s)
        # dict for positionalParam -> {key1:'a',key2:'b'}

        query = "INSERT INTO {}({}) VALUES ({})".format(tableName,
                                                        ','.join(map(str,columnNames)),
                                                        ','.join(map(str,["%({})s".format(k) for k in columnNames])))
        values = dict (zip (columnNames,columnValues))
        c.execute(query, values)
        print(c.query)
        c.connection.commit()
    except Exception as e:
        e.with_traceback()


create_ddl_table()
check_connection()
insert_values(str("t_classroom"),list(["cid","cname","csection"]), list([1,"Manoj","A"]))
insert_values(str("t_classroom"),list(["cid","cname","csection"]), list([1,"LKG","A"]))
check_table_entries()



