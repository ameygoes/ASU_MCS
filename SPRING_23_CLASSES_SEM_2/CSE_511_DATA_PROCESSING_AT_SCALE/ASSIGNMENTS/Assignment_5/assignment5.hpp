#ifndef assignment5_h
#define assignment5_h

#include <rocksdb/db.h>
#include <rocksdb/options.h>
#include <vector>

rocksdb::DB* create_kvs(const std::string& csv_file_path, const std::string& db_path);
std::vector<std::string> multi_get(rocksdb::DB* db, const std::vector<std::string>& keys);
std::vector<std::string> iterate_over_range(rocksdb::DB* db, const std::string& start_key, const std::string& end_key);
rocksdb::Status delete_key(rocksdb::DB* db, const std::string& key);

#endif /* assignment5_h */
