import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    - Loads the data stored in Amazon (Simple Storage Service) S3 bucket to the staging tables
    
    - Uses SQL queries listed in copy_table_queries
    """
    print("--------LOADING DATA FROM S3 INTO STAGING TABLES---------\n")
    for query in copy_table_queries:
        print("Executing------------ "+ query)
        cur.execute(query)
        conn.commit()
        print("Query Execution Finished \n")


def insert_tables(cur, conn):
    """
    - Extracts the data from staging tables
    
    - Transforms it as per requirement
    
    - Loads the extracted and transformed data to individual tables
    
    - Uses SQL queries listed in insert_table_queries
    """
    print("--------LOADING DATA INTO TABLES---------\n")
    for query in insert_table_queries:
        print("Executing------------ "+ query)
        cur.execute(query)
        conn.commit()
        print("Query Execution Finished \n")

def main():
    """
    - Loads the data stored in S3 bucket to the staging tables. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Extracts, transforms and loads the data to individual tables
    
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()