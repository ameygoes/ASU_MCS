# Import required libraries
import traceback
import psycopg2
import psycopg2.extras
import csv
import json
import math


########################## Setup Functions ##########################

def get_open_connection(username='postgres', password='postgres', dbname='postgres', host="127.0.0.1"):
    """
    Connect to the database and return connection object
    
    Returns:
        connection: The database connection object.
    """

    return psycopg2.connect(f"dbname='{dbname}' user='{username}' host='{host}' password='{password}'")


def create_db(dbname):
    """
    Create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    """

    # Connect to the database with default values
    con = get_open_connection()
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute(f"select count(*) from pg_catalog.pg_database where datname='{dbname}'")
    if cur.fetchone()[0] == 0:
        cur.execute(f'create database {dbname}')  # Create the database
    else:
        print(f'A database named "{dbname}" already exists')

    # Clean up
    cur.close()
    con.close()


def delete_db(dbname):
    """
    Let it go...  
    Deleting the database provided to you
    """

    con = get_open_connection(dbname={dbname})
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    cur.execute(f'drop database {dbname}')
    
    cur.close()
    con.close()


def delete_all_public_tables(connection):
    """
    Deleting all the tables in the database 
    """

    cur = connection.cursor()
    table_list = []

    cur.execute("select table_name from information_schema.tables where table_schema = 'public'")
    for row in cur:
        table_list.append(row[0])

    for table in table_list:
        cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
        connection.commit()

    cur.close()


#####################################################################



########################### Tester Support ##########################

def get_count_range_partition(data_table_name, partition_table_name, num_partitions, connection, column_to_partition):
    """
    Get number of rows for each partition

    Args:
        table_name (str): Name of table 
        num_partitions (int): Number of partitions
        connection: DB Connection object

    Returns:
        count_list (list): A list of row counts for each partition
    """

    count_list = []

    with connection.cursor() as cursor:

        # Get min and max values in the column and then find ranges
        cursor.execute(f"SELECT MIN({column_to_partition}) FROM {data_table_name}")
        min_val = cursor.fetchone()[0]
        cursor.execute(f"SELECT MAX({column_to_partition}) FROM {data_table_name}")
        max_val = cursor.fetchone()[0]

        interval = math.ceil((max_val - min_val + 1)/num_partitions)
        lower_bound = min_val

        for i in range(0, num_partitions):
            cursor.execute(f"select count(*) from {data_table_name} where {column_to_partition} >= {lower_bound} and {column_to_partition} < {lower_bound + interval}")
            lower_bound += interval
            count_list.append(int(cursor.fetchone()[0]))

    return count_list


def get_count_round_robin_partition(table_name, num_partitions, connection):
    '''
    Get the number of rows for each partition using round-robin partitioning.

    Args:
        table_name (str): Name of the table.
        num_partitions (int): Number of partitions.
        connection: DB Connection object.

    Returns:
        count_list (list): A list containing the number of rows in each partition.
    '''

    count_list = []
    with connection.cursor() as cur:    
        for i in range(0, num_partitions):
            cur.execute(f"select count(*) from (select *, row_number() over () from {table_name}) as temp where (row_number-1)%{num_partitions}= {i}")
            count_list.append(int(cur.fetchone()[0]))

    return count_list


#####################################################################



########################### Tester Helper ###########################

def check_partition_count(cursor, expected_partitions, prefix):
    """
    Checks the number of partitions created against the expected number.

    Args:
        cursor (cursor object): The cursor object for the database connection.
        expected_partitions (int): The number of expected partitions.
        prefix (str): The prefix used in the partition names.

    Raises:
        Exception: If the actual number of partitions created does not match the expected number.
    """
    cursor.execute(
        f"SELECT COUNT(table_name) FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '{prefix}_%';"
    )
    count = int(cursor.fetchone()[0])
    if count != expected_partitions:
        raise Exception(f"Range partitioning not done properly. Expected {expected_partitions} table(s) but found {count} table(s).")



def total_rows_in_all_partitions(cur, n, range_partition_table_prefix, partition_start_index):
    """
    Returns the total number of rows across all range partitions.

    Args:
        cur: Cursor object for the database connection.
        n (int): Number of partitions.
        range_partition_table_prefix (str): Prefix for the range partition table names.
        partition_start_index (int): Starting index for the range partition tables.

    Returns:
        int: Total number of rows across all range partitions.
    """
    selects = []
    for i in range(partition_start_index, n + partition_start_index):
        selects.append(f"SELECT * FROM {range_partition_table_prefix}{i}")
    cur.execute(f"SELECT COUNT(*) FROM ({' UNION ALL '.join(selects)}) AS T")
    count = int(cur.fetchone()[0])

    return count


def test_range_and_robin_partitioning(n, connection, range_partition_table_prefix, partition_start_index, actual_rows_in_input_file):
    """
    Tests the range and round-robin partitioning.

    Args:
        n (int): Number of partitions.
        connection: Database connection.
        range_partition_table_prefix (str): Prefix for the range partition table names.
        partition_start_index (int): Starting index for the range partition tables.
        actual_rows_in_input_file (int): Actual number of rows in the input file.

    Raises:
        Exception: If any of the tests fail.
    """
    with connection.cursor() as cur:
        if not isinstance(n, int) or n < 0:
            # Test 1: Check the number of tables created, if 'n' is invalid
            check_partition_count(cur, 0, range_partition_table_prefix)
        else:
            # Test 2: Check the number of tables created, if all args are correct
            check_partition_count(cur, n, range_partition_table_prefix)

            count = total_rows_in_all_partitions(cur, n, range_partition_table_prefix, partition_start_index)
            # Test 3: Test Completeness
            if count < actual_rows_in_input_file:
                raise Exception(f"Completeness property of Range Partitioning failed. Expected {actual_rows_in_input_file} rows after merging all tables, but found {count} rows")
            # Test 4: Test Disjointness
            elif count > actual_rows_in_input_file:
                raise Exception(f"Dijointness property of Range Partitioning failed. Expected {actual_rows_in_input_file} rows after merging all tables, but found {count} rows")
            # Test 5: Test Reconstruction
            elif count != actual_rows_in_input_file:
                raise Exception(f"Reconstruction property of Range Partitioning failed. Expected {actual_rows_in_input_file} rows after merging all tables, but found {count} rows")


def test_range_robin_insert(expected_table_name, connection, column_id):
    """
    Test if the data for a given item and user was inserted successfully.

    Args:
        expected_table_name (str): The name of the expected table.
        connection: The database connection.
        column_id (str): The ID of the row.

    Returns:
        bool: True if the data was inserted successfully, False otherwise.
    """
    with connection.cursor() as cur:
        cur.execute(
            f"SELECT COUNT(*) FROM {expected_table_name} WHERE id = '{column_id}'")
        
        count = int(cur.fetchone()[0])
    
    if count != 1:
        return False
        
    return True


def test_each_range_partition(data_table_name, partition_table_name, n, connection, range_partition_table_prefix, column_to_partition):
    """
    Test if each range partition has the correct number of rows.

    Args:
        table_name (str): The name of the input table.
        n (int): The number of partitions.
        connection: The database connection.
        range_partition_table_prefix (str): The prefix for the range partition tables.

    Raises:
        Exception: If a range partition has the incorrect number of rows.
    """

    count_list = get_count_range_partition(data_table_name, partition_table_name, n, connection, column_to_partition)
    with connection.cursor() as cur:
        for i in range(0, n):
            cur.execute(f"SELECT COUNT(*) FROM {range_partition_table_prefix}{i}")
            count = int(cur.fetchone()[0])

            if count != count_list[i]:
                raise Exception(f"{range_partition_table_prefix}{i} has {count} rows while the correct number should be {count_list[i]}")


def test_each_round_robin_partition(table_name, n, connection, round_robin_partition_table_prefix):
    """
    Test if each round-robin partition has the correct number of rows.

    Args:
        table_name (str): The name of the input table.
        n (int): The number of partitions.
        connection: The database connection.
        round_robin_partition_table_prefix (str): The prefix for the round-robin partition tables.

    Raises:
        Exception: If a round-robin partition has the incorrect number of rows.
    """

    count_list = get_count_round_robin_partition(table_name, n, connection)
    with connection.cursor() as cur:
        for i in range(0, n):
            cur.execute(
                f"SELECT COUNT(*) FROM {round_robin_partition_table_prefix}{i}"
            )
            count = cur.fetchone()[0]
            if count != count_list[i]:
                raise Exception(f"{round_robin_partition_table_prefix}{i} has {count} rows while the correct number should be {count_list[i]}")


def count_rows_in_csv(file_path, header=True):
    """
    Counts the number of rows in a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        header (bool): Whether or not the CSV file has a header row.

    Returns:
        lines (int): The total number of rows in the CSV file.
    """

    f = open(file_path, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    if header:
        return lines - 1
    else:
        return lines
        

def get_headers(file_path):
    """
    Get the header row of the input csv file

    Returns:
        header_list: The list of headers in the file
    """

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

    return fieldnames


def range_insert(table_name, connection, data_dict):
    """
    Use this function to find and insert data into the correct partition (range based).

    Args:
        table_name (str): The base name of the table.
        data_dict (dict): The dictionary containing the data to be inserted into the partition.
        connection: The database connection object.
    """

    cursor = connection.cursor()

    # Data cleaning and pre processing
    # If you made it this far looking for an answer, its actually quite simple
    # psycopg2 does not take empty strings as input, use None instead of ""
    # You can condence the loop below in a single line to make it efficient
    query_data_list = []
    
    def read_data():
        for _, value in data_dict.items():
            if value == "":
                query_data_list.append(None)
            else: 
                query_data_list.append(value)
        yield query_data_list

    # Inserting data
    psycopg2.extras.execute_values(cursor, f"INSERT INTO {table_name} VALUES %s", read_data(), page_size=100000)

    connection.commit()
    cursor.close()


def round_robin_insert(table_name, connection, data_dict):
    """
    Use this function to find and insert data into the correct partition (round robin based).

    Args:
        table_name (str): The base name of the table.
        data_dict (dict): The dictionary containing the data to be inserted into the partition.
        connection: The database connection object.
    """

    cursor = connection.cursor()

    # Data cleaning and pre processing
    # If you made it this far looking for an answer, its actually quite simple
    # psycopg2 does not take empty strings as input, use None instead of ""
    # You can condence the loop below in a single line to make it efficient
    query_data_list = []
    
    def read_data():
        for _, value in data_dict.items():
            if value == "":
                query_data_list.append(None)
            else: 
                query_data_list.append(value)
        yield query_data_list

    # Inserting data
    psycopg2.extras.execute_values(cursor, f"INSERT INTO {table_name} VALUES %s", read_data(), page_size=100000)

    connection.commit()
    cursor.close()

#####################################################################



########################### The Real Deal ###########################

def test_load_data(my_assignment, table_name, file_path, connection, rows_in_file, header_path):
    """
    Tests the load data function.

    Args:
        my_assignment: an instance of the my_assignment class.
        table_name (str): Name of table to be tested.
        file_path (str): Path to input file.
        connection: An open connection to the database.
        rows_in_file (int): Number of rows in the input file provided for assertion.

    Returns:
        [bool, Exception]: A list containing a boolean value indicating whether the tests passed or failed, and an exception object if the tests failed.
    """
    try:
        my_assignment.load_data(table_name, file_path, connection, header_path)
        
        # Count the number of rows inserted
        with connection.cursor() as cur:
            cur.execute(f'SELECT COUNT(*) from {table_name}')
            count = int(cur.fetchone()[0])
            if count != rows_in_file:
                raise Exception(f"Expected {rows_in_file} rows, but {count} rows in '{table_name}' table")

    except Exception as e:
        traceback.print_exc()
        return [False, e]
        
    return [True, None]


def test_range_partition(my_assignment, data_table_name, partition_table_name, n, 
                         connection, partition_start_index, actual_rows_in_input_file, 
                         header_file, column_to_partition):
    """
    Tests the range partition function.

    Args:
        my_assignment: Object containing the rangePartition method to be tested.
        table_name (str): Name of table to be partitioned.
        n (int): Number of partitions.
        connection: Connection object for the database.
        partition_start_index (int): Index at which the table names start.
        actual_rows_in_input_file (int): Number of rows in the input file.

    Returns:
        [bool, Exception]: A list containing a boolean value indicating whether the tests passed or failed, and an exception object if the tests failed.
    """
    try:
        # my_assignment.range_partition(table_name, n, connection)
        my_assignment.range_partition(data_table_name, partition_table_name, n, header_file, column_to_partition, connection)
        test_range_and_robin_partitioning(n, connection, partition_table_name, partition_start_index, actual_rows_in_input_file)
        test_each_range_partition(data_table_name, partition_table_name, n, connection, partition_table_name, column_to_partition)
        return [True, None]
    except Exception as e:
        if str(e) == "Function yet to be implemented!":
            print(e)
        else:
            traceback.print_exc()
        return [False, e]


def test_range_insert(my_assignment, table_name, connection, data_dict, expected_table_index):
    """
    Tests the range insert function by checking whether the tuple is inserted in the expected table you provide.

    Args:
        my_assignment: Instance of the class whose method needs to be tested. Not used anymore
        table_name (str): The name of the table being used.
        connection: The connection object for connecting to the database.
        data_dict (dict): Dictionary containing data 
        expected_table_index (int): The expected table index to which the record has to be saved.

    Raises:
        Exception: If the test fails and the tuple could not be found in the expected table.
    """
    try:
        expected_table_name = f"{table_name}{expected_table_index}"
        range_insert(table_name, connection, data_dict)

        if not test_range_robin_insert(expected_table_name, connection, data_dict["id"]):
            raise Exception(f"Range insert failed! Could not find tuple in {expected_table_name} table")
    except Exception as e:
        if str(e) == "Function yet to be implemented!":
            print(e)
        else:
            traceback.print_exc()
        return [False, e]

    return [True, None]


def test_round_robin_partition(my_assignment, data_table_name, partition_table_name, n, 
                         connection, partition_start_index, actual_rows_in_input_file, 
                         header_file, column_to_partition):
    """
    Tests the round robin partitioning.

    Args:
        my_assignment: Object containing the roundRobinPartition method to be tested.
        table_name (str): Name of table to be partitioned.
        number_of_partitions (int): Number of partitions.
        connection: Connection object for the database.
        partition_start_index (int): Index at which the table names start.
        actual_rows_in_input_file (int): Number of rows in the input file.

    Returns:
        [bool, Exception]: A list containing a boolean value indicating whether the tests passed or failed, and an exception object if the tests failed.
    """
    try:
        my_assignment.round_robin_partition(data_table_name, partition_table_name, n, header_file, connection)
        test_range_and_robin_partitioning(n, connection, partition_table_name, partition_start_index, actual_rows_in_input_file)
        test_each_round_robin_partition(partition_table_name, n, connection, partition_table_name)

    except Exception as e:
        if str(e) == "Function yet to be implemented!":
            print(e)
        else:
            traceback.print_exc()
        return [False, e]
    return [True, None]


def test_round_robin_insert(my_assignment, table_name, connection, data_dict, expected_table_index):
    """Tests the round robin insert function by checking whether the tuple is inserted in the expected table.

    Args:
        my_assignment: Object containing the roundrobininsert method to be tested.
        table_name (str): Name of the table.
        connection: Connection object for the database.
        data_dict (dict): Dictionary containing data 
        expected_table_index (int): The index of the expected table.

    Returns:
        [bool, Exception]: A list containing a boolean indicating success or failure, and an exception (if any).
    """
    try:
        expected_table_name = f"{table_name}{expected_table_index}"
        round_robin_insert(table_name, connection, data_dict)
        if not test_range_robin_insert(expected_table_name, connection, data_dict["id"]):
            raise Exception(f"Round robin insert failed! Couldn't find tuple in {expected_table_name} table")
    except Exception as e:
        if str(e) == "Function yet to be implemented!":
            print(e)
        else:
            traceback.print_exc()
        return [False, e]
    return [True, None]
