flag=$1

# TRUNCATE TABLES
psql -d postgres -a -f truncateTable.sql

# Get Counts
psql -d postgres -a -f getCounts

if [ "$flag" = true ] ; then
    # CopyDataUsing \Copy
	time psql -d postgres -a -f copyDataUsingCopy.sql >> copyDataLogs.log
	
	# Get Counts
	psql -d postgres -a -f getCounts

	# TRUNCATE TABLES
	psql -d postgres -a -f truncateTable.sql
fi

# CopyDataUsing \postgres
time sh assignment1.sh >> pgBulkLoadLogs.log
