# Import required libraries
import psycopg2
import traceback
import test_helper
import assignment3
import json


dbname = "assignment3"
count_of_partitions = 5

# Table nomenclature
data_table_name = "subreddits"
column_to_partition = "created_utc"
range_table_prefix = 'range_part'
rrobin_table_prefix = 'rrobin_part'

# Data files
input_file_path = './subreddits.csv'
header_path = "./headers.json"
insert_data_path_1 = "./insert1.json"
insert_data_path_2 = "./insert2.json"
insert_data_path_3 = "./insert3.json"

# Misc
rows_in_input = 914067

# Yet to implement properly
# What do you want to test:
load_data = True
range_partion = True
round_robin_partition = True


def main():
        
    try:
        test_helper.create_db(dbname)
        with test_helper.get_open_connection(dbname=dbname) as conn:
            
            # Get the count of rows in your input
            # rows_in_input = test_helper.count_rows_in_csv(input_file_path)
            # headers = test_helper.get_headers(input_file_path)

            if load_data:
                # Connect to the DB and clean up
                conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                test_helper.delete_all_public_tables(conn)
                # test_helper.delete_all_public_triggers(conn)

                # Test the loading
                print("----------------------------------------------------------------------------")
                print("Testing load_data function")
                [result, e] = test_helper.test_load_data(assignment3, data_table_name, input_file_path, conn, rows_in_input, header_path)
                if result:
                    print("load_data function pass!")
                print("----------------------------------------------------------------------------\n")

            with open(insert_data_path_1) as json_data:
                data_dict_1 = json.load(json_data)
            with open(insert_data_path_2) as json_data:
                data_dict_2 = json.load(json_data)
            with open(insert_data_path_3) as json_data:
                data_dict_3 = json.load(json_data)
            
            if range_partion:
                # Test the range partition function
                print("----------------------------------------------------------------------------")
                print("Testing range_partition function")
                [result, e] = test_helper.test_range_partition(assignment3, data_table_name, range_table_prefix, count_of_partitions, conn, 0, rows_in_input, header_path, column_to_partition)
                if result:
                    print("range_partition function pass!")
                print("----------------------------------------------------------------------------\n")


                # Test the range insert function
                # ALERT: Use only one at a time i.e. uncomment only one line at a time and run the script
                print("----------------------------------------------------------------------------")
                print("Testing range_insert function")
                [result, e] = test_helper.test_range_insert(assignment3, range_table_prefix, conn, data_dict_1, '0')
                # [result, e] = test_helper.test_range_insert(assignment3, table_name, conn, data_dict, '0')
                if result:
                    print("range_insert function pass!")
                print("----------------------------------------------------------------------------\n")

            if round_robin_partition:
                # Test the round robin partition function
                print("----------------------------------------------------------------------------")
                print("Testing round_robin_partition function")
                [result, e] = test_helper.test_round_robin_partition(assignment3, data_table_name, rrobin_table_prefix, count_of_partitions, conn, 0, rows_in_input, header_path, column_to_partition)
                if result:
                    print("round_robin_partition function pass!")
                print("----------------------------------------------------------------------------\n")
                
                # Test the round robin insert function
                print("----------------------------------------------------------------------------")
                print("Testing round_robin_insert function")
                # ALERT: This is pretty static in the rows_in_input. You might face issues on re-runs
                [result, e] = test_helper.test_round_robin_insert(assignment3, rrobin_table_prefix, conn, data_dict_1, str(rows_in_input%5))
                [result, e] = test_helper.test_round_robin_insert(assignment3, rrobin_table_prefix, conn, data_dict_2, str(rows_in_input%5 + 1))
                [result, e] = test_helper.test_round_robin_insert(assignment3, rrobin_table_prefix, conn, data_dict_3, str(rows_in_input%5 + 2))
                if result:
                    print("round_robin_insert function pass!")
                print("----------------------------------------------------------------------------\n")

            # Delete or not? I say yay, but your opinion might differ
            choice = input('Press d to Delete all tables? ')
            if (choice == 'd'):
                test_helper.delete_all_public_tables(conn)

    # Print the exepection in case any occurs
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()