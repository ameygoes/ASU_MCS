export PGPASSWORD=postgres

# CREATE TABLES
psql -d postgres -U postgres -a -f createTables.sql

# TIME THE LOADING OF AUTHORS
pg_bulkload -i './authors.csv' -O postgres.authors -l ./opAuthors.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -U postgres -h 127.0.0.1

# TIME THE LOADING OF SUBREDDITS
pg_bulkload -i './subreddits.csv' -O postgres.subreddits -l ./opSubreddits.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -U postgres -h 127.0.0.1

# TIME THE LOADING OF COMMENTS
pg_bulkload -i './comments.csv' -O postgres.comments -l ./opComments.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -U postgres -h 127.0.0.1

# TIME THE LOADING OF SUBMISSIONS
pg_bulkload -i './submissions.csv' -O postgres.submissions -l ./opSubmissions.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -U postgres -h 127.0.0.1