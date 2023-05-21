// Test the assignment5.cc file

#include "assignment5.hpp"
#include <iostream>

// Namespaces
using namespace std;
using namespace rocksdb;


int main() {

    // 0. set up the paths
    // Do not change these paths
    const std::string csv_file_path = "subreddits.csv";
    const std::string db_path = "./test/subreddits_rdb";

    // create the KVS
    rocksdb::DB* db = create_kvs(csv_file_path, db_path);
    if (db != nullptr) {
        cout << "RocksDB may be created successfully from CSV file." << std::endl;
    } else {
        cout << "Failed to create RocksDB from CSV file." << std::endl;
    }


    // multi get
    vector<string> multi_get_keys = {"2qh1r_display_name", "2qh1k_display_name", "2qh1a_display_name", "2qh1b_display_name"};
    vector<string> multi_get_results = multi_get(db, multi_get_keys);

    // Convert the vector of keys to a vector of Slice objects
    for (auto result : multi_get_results) {
        // You should see the display_name of the subreddit
        // One display_name per line because of endl
        cout << result << endl;
    }


    // iterate over range of keys
    // Only return the display_name of the subreddit
    vector<string> results = iterate_over_range(db, "2qh0x", "2qh1q");
    for (auto result : results) {
        // You should see the display_name of the subreddit
        // One display_name per line because of endl
        cout << result << endl;
    }


    // delete a particular key
    Status s = delete_key(db, "2cneq_id");
    // You should see "Maybe successfully deleted key." if the key was deleted and your code is correct
    if (s.ok()) {
        cout << "Maybe successfully deleted key." << endl;
    } else {
        cout << "Failed to delete key." << endl;
    }
    
    
    // Implementing your own tests is highly recommended!!

    return 0;
}
