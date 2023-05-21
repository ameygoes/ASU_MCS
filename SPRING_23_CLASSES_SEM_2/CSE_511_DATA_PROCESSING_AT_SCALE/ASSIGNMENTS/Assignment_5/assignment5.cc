// General Libraries
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "csv.hpp"
#include <sstream>

// RocksDB Libraries
#include <rocksdb/db.h>
#include <rocksdb/options.h>
#include <rocksdb/status.h>


// Namespaces
using namespace std;
using namespace rocksdb;

using ROCKSDB_NAMESPACE::DB;
using ROCKSDB_NAMESPACE::DBOptions;
using ROCKSDB_NAMESPACE::Options;
using ROCKSDB_NAMESPACE::Status;
using ROCKSDB_NAMESPACE::WriteBatch;
using ROCKSDB_NAMESPACE::WriteOptions;
using ROCKSDB_NAMESPACE::ReadOptions;
using ROCKSDB_NAMESPACE::Slice;


// Function to create a RocksDB instance and insert data from a CSV file
DB* create_kvs(const string& csv_file_path, const string& db_path) {
    // Open the CSV file
    csv::CSVReader reader(csv_file_path);
    // Get the column names
    vector<string> header = reader.get_col_names();

    // Configure the RocksDB instance
    Options options;
    options.create_if_missing = true;
    DB* db;
    Status status = DB::Open(options, db_path, &db);

    if (!status.ok()) {
        cerr << "Error opening RocksDB instance: " << status.ToString() << endl;
        return nullptr;
    }

    // Insert data into the RocksDB instance
    WriteBatch batch;
    for (csv::CSVRow& row : reader) {
        string id = row["id"].get<string>();
        for (size_t i = 0; i < row.size(); i++) {
            string key = id + "_" + header[i];
            string value = row[i].get<string>();
            batch.Put(key, value);
        }
    }

    status = db->Write(WriteOptions(), &batch);
    if (!status.ok()) {
        cerr << "Error inserting data into RocksDB: " << status.ToString() << endl;
        return nullptr;
    }

    return db;
}


vector<string> multi_get(DB* db, const vector<string>& keys) {
    // Initialize vectors for keys, values, and statuses
    vector<Slice> db_keys;
    vector<string> db_values;
    vector<Status> statuses;

    // Convert keys to slices
    for (const auto& key : keys) {
        db_keys.emplace_back(key);
    }

    // Retrieve values using MultiGet()
    statuses = db->MultiGet(ReadOptions(), db_keys, &db_values);

    // Check for errors in the statuses
    for (const auto& status : statuses) {
        if (!status.ok()) {
            cerr << "Error: " << status.ToString() << endl;
        }
    }

    // Return the fetched values
    return db_values;
}


// Function to iterate over a range of keys and return the corresponding values
vector<string> iterate_over_range(DB* db, const string& start_key, const string& end_key) {
    vector<string> result;

    Iterator* it = db->NewIterator(ReadOptions());
    for (it->Seek(start_key);  it->Valid() && it->key().ToString() < end_key;  it->Next()) {
        string key = it->key().ToString();
        string endPart = "_display_name";

        if (key.find(endPart) != string::npos) {
            result.emplace_back(it->value().ToString());
        }
    }
    assert(it->status().ok()); // Check for any errors found during the scan
    delete it;
    return result;
}

// Function to delete a particular comment from the kvs
Status delete_key(DB* db, const string& key) {
    WriteOptions write_options;
    return db->Delete(write_options, key);
}
