import pyodbc

USER = "ZEREF"
PASSWD = "toor"
HOST = "localhost"
port = "5432"


def myConnection():
    try:
        connection = psycopg2.connect(user = "ZEREF",
                                  password = "toor",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)


def close_con(connection):
    if(connection, cursor):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")





