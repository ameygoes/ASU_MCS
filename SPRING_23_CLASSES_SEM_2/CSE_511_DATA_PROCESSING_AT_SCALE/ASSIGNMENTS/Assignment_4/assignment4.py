# Import required libraries
import psycopg2
import psycopg2.extras
import json
import csv
import math 


# Lets define some of the essentials
# We'll define these as global variables to keep it simple
username = "postgres"
password = "postgres"
dbname = "assignment4"
host = "127.0.0.1"

def getNumberOfPartitionTables(connection, parent_partition_table_name):
    
    cursor = connection.cursor()

    cursor.execute(f"SELECT inhrelid::regclass FROM pg_inherits WHERE inhparent = '{parent_partition_table_name}'::regclass;")

    result = cursor.fetchall()

    return len(result)


def point_query(parent_partition_table_name, utc_val, save_table_name, connection):
    """
    Use this function to perform a point query on the given table. 
    The table input is either range (range_part) or round-roublin (rrobin_part) partitioned.
    The output should be saved in a table with the name "save_table_name".
    Make sure the ouptu is stored in asc order

    Args:
        parent_partition_table_name (str): The name of the table containing the partitions to be queried.
        utc_val (str): The UTC value to be queried.
        save_table_name (str): The name of the table where the output is to be saved.
        connection: The database connection object.
    """
    partitionTableCount = getNumberOfPartitionTables(connection, parent_partition_table_name)

    queryList = [] 
    for i in range(partitionTableCount):
        query = f"SELECT * FROM {parent_partition_table_name}{i} WHERE created_utc={utc_val}"
        queryList.append(query)
    
    queryToBeRun = "SELECT * INTO TABLE {} FROM ({}) AS T".format(save_table_name, ' UNION ALL '.join(queryList))

    queryToBeRun = queryToBeRun + " ORDER BY created_utc ASC"
    cursor = connection.cursor()
    cursor.execute(queryToBeRun)
    connection.commit()


def range_query(parent_partition_table_name, utc_min_val, utc_max_val, save_table_name, connection):
    """
    Use this function to perform a range query on the given table. 
    The table is either range (range_part) or round-roublin (rrobin_part) partitioned.
    The output should be saved in a table with the name "save_table_name".
    Make sure the ouptu is stored in asc order

    Args:
        parent_partition_table_name (str): The name of the table containing the partitions to be queried.
        utc_min_val (str): The minimum UTC value to be queried.
        utc_max_val (str): The maximum UTC value to be queried.
        save_table_name (str): The name of the table where the output is to be saved.
        connection: The database connection object.
    """
    partitionTableCount = getNumberOfPartitionTables(connection, parent_partition_table_name)

    queryList = []
    for i in range(partitionTableCount):
        query = f"SELECT * FROM {parent_partition_table_name}{i} WHERE created_utc > {utc_min_val} AND created_utc <={utc_max_val}"
        queryList.append(query)
    
    queryToBeRun = "SELECT * INTO TABLE {} FROM ({}) AS T".format(save_table_name, ' UNION ALL '.join(queryList))

    queryToBeRun = queryToBeRun + " ORDER BY created_utc ASC"

    cursor = connection.cursor()
    cursor.execute(queryToBeRun)
    connection.commit()

    