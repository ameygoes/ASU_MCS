# You may need to moify the following variables to match your environment.
ROCKSDB_DIR = /root/rocksDB/rocksdb-7.10.2

CC = g++
CFLAGS = -std=c++17 -Wall -Wextra
LDFLAGS = -L$(ROCKSDB_DIR) -lrocksdb -lpthread -lrt -ldl -lsnappy -lgflags -lz -lbz2 -llz4 -lzstd
CXXFLAGS = -I$(ROCKSDB_DIR)/include

.PHONY: clean 

all: tester test2

tester: tester.cc assignment5.cc assignment5.hpp 
	$(CXX) $(CFLAGS) $(CXXFLAGS) assignment5.cc tester.cc $(LDFLAGS) -o tester 

test2: hello.cc
	$(CXX) $(CFLAGS) $(CXXFLAGS) hello.cc tester.cc $(LDFLAGS) -o tester 

clean:
	rm -f assignment5 tester

