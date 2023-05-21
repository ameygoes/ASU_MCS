# Import required libraries
# Do not install/import any additional libraries
import psycopg2
import psycopg2.extras
import json
import csv
import math 


# Lets define some of the essentials
# We'll define these as global variables to keep it simple
username = "postgres"
password = "postgres"
dbname = "assignment3"
host = "127.0.0.1"


def get_open_connection():
    """
    Connect to the database and return connection object
    
    Returns:
        connection: The database connection object.
    """

    return psycopg2.connect(f"dbname='{dbname}' user='{username}' host='{host}' password='{password}'")

def create_partitioned_table(connection, header_file, query, flag, data):
    cursor = connection.cursor()
    with open(header_file) as json_data:
        header_dict = json.load(json_data)
    
    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    
    if flag:
        query = query.format(data[0], table_rows_formatted, data[1])
    else:
        query = query.format(data[0], table_rows_formatted)
    cursor.execute(query)
    connection.commit()

def load_data(table_name, csv_path, connection, header_file):
    """
    Create a table with the given name and load data from the CSV file located at the given path.

    Args:
        table_name (str): The name of the table where data is to be loaded.
        csv_path (str): The path to the CSV file containing the data to be loaded.
        connection: The database connection object.
        header_file (str): The path to where the header file is located
    """

    cursor = connection.cursor()

    # Creating the table
    with open(header_file) as json_data:
        header_dict = json.load(json_data)

    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_rows_formatted}
            )'''

    cursor.execute(create_table_query)
    connection.commit()


    # # TODO: Implement code to insert data here
    with open(csv_path, 'r') as csv_file:
        insert_query = f"COPY {table_name} ({', '.join(header_dict.keys())}) FROM STDIN WITH CSV HEADER"
        cursor.copy_expert(insert_query, csv_file)

def range_partition(data_table_name, partition_table_name, num_partitions, header_file, column_to_partition, connection):
    """
    Use this function to partition the data in the given table using a range partitioning approach.

    Args:
        data_table_name (str): The name of the table that contains the data loaded during load_data phase.
        partition_table_name (str): The name of the table to be created for partitioning.
        num_partitions (int): The number of partitions to create.
        header_file (str): path to the header file that contains column headers and their data types
        column_to_partition (str): The column based on which we are creating the partition.
        connection: The database connection object.
    """
    cursor = connection.cursor()

    # CREATE PARTITION TABLE AS STATED IN DOCUMENT
    partionTableSQL = "CREATE TABLE {} ({}) PARTITION BY RANGE ({})"
    tuplee = (partition_table_name, column_to_partition)
    create_partitioned_table(connection=connection, header_file=header_file, query=partionTableSQL, flag=True, data=tuplee)

    # GET MIN AND MAX VALUE OF UTC COL AS GIVEN IN THE HINT
    cursor.execute(f"SELECT MIN({column_to_partition}), MAX({column_to_partition}) FROM {data_table_name}")
    min_value, max_value = cursor.fetchone()
    
    # Calculate the range for each partition
    partition_range = (max_value - min_value + 1) / num_partitions
    partition_ranges = [(min_value + partition_range*i, min_value + partition_range*(i+1)) for i in range(num_partitions)]

    for i in range(num_partitions):
        partition_name = f"{partition_table_name}{i}"
        minBnd, maxBnd = partition_ranges[i]
        partition_query = f"CREATE TABLE {partition_name} PARTITION OF {partition_table_name} FOR VALUES FROM ({minBnd}) TO ({maxBnd})"
        cursor.execute(partition_query)

    # FINALLY INSERT DATA IN PARTITIONED TABLE
    cursor.execute(f"INSERT INTO {partition_table_name} SELECT * FROM {data_table_name}")
    connection.commit()

def round_robin_partition(data_table_name, partition_table_name, num_partitions, header_file, connection):
    """
    Use this function to partition the data in the given table using a round-robin approach.

    Args:
        data_table_name (str): The name of the table that contains the data loaded during load_data phase.
        partition_table_name (str): The name of the table to be created for partitioning.
        num_partitions (int): The number of partitions to create.
        header_file (str): path to the header file that contains column headers and their data types
        connection: The database connection object.
    """
    cursor = connection.cursor()
    with open(header_file) as json_data:
        header_dict = json.load(json_data)
    
    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {partition_table_name} ({table_rows_formatted})')
    
    for i in range(num_partitions):
        query="CREATE TABLE {partition_table_name}{table_num} () INHERITS ({partition_table_name});".format(partition_table_name=partition_table_name,table_num=i)
        cursor.execute(query)
    
    headers = (", ".join(f"{header} " for header, header_type in header_dict.items()))
    
    

    for i in range(num_partitions):
        query = f'''INSERT INTO {partition_table_name}{i} SELECT {headers} FROM (SELECT *, ROW_NUMBER() OVER () FROM {data_table_name}) as data_tabble WHERE MOD(ROW_NUMBER-1,{num_partitions})={i};'''
        cursor.execute(query)

    connection.commit()


    trigger='''
           CREATE OR REPLACE FUNCTION round_robin_insert()
            RETURNS TRIGGER AS
            $$
            DECLARE
                partition_table_name TEXT := TG_ARGV[0];
                num_partitions INTEGER := TG_ARGV[1];
                partitionCNT INTEGER;
                EndTable TEXT;
            BEGIN
                EXECUTE format('SELECT COUNT(*) FROM %I', partition_table_name) INTO partitionCNT;
                EndTable := partition_table_name || (partitionCNT % num_partitions)::TEXT;
                EXECUTE FORMAT('INSERT INTO %I VALUES ($1.*)', EndTable) USING NEW;
                RAISE NOTICE 'Inserted into %', EndTable;
                RETURN NULL;
            END;
            $$
            LANGUAGE plpgsql;

        '''
    cursor.execute(trigger)
    
    create_trigger_query = f'''
        CREATE TRIGGER RoundRobin
        BEFORE INSERT ON {partition_table_name}
        FOR EACH ROW
        EXECUTE FUNCTION RoundRobin_function(%s, %s);
    '''
    cursor.execute(create_trigger_query, (partition_table_name, num_partitions))

def delete_partitions(table_name, num_partitions, connection):
    """
    This function in NOT graded and for your own testing convinience.
    Use this function to delete all the partitions that are created by you.

    Args:
        table_name (str): The name of the table containing the partitions to be deleted.
        num_partitions (int): The number of partitions to be deleted.
        connection: The database connection object.
    """

    cursor = connection.cursor()
    for i in range(num_partitions):
        cursor.execute(f'''DROP table {table_name}{i};''')
    cursor.close()