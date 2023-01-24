# CREATE TABLES
psql -d postgres -a -f createTable.sql

# TIME THE LOADING OF AUTHORS
pg_bulkload -i '/mnt/c/Amey/ASU/ASU_MCS/SPRING_23_CLASSES_SEM_2/CSE_511_DATA_PROCESSING_AT_SCALE/ASSIGNMENTS/Assignment_1/Data/authors.csv' -O authors -l /root/pg_assignment_1/opAuthors.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -h 127.0.0.1

# TIME THE LOADING OF SUBREDDITS
pg_bulkload -i '/mnt/c/Amey/ASU/ASU_MCS/SPRING_23_CLASSES_SEM_2/CSE_511_DATA_PROCESSING_AT_SCALE/ASSIGNMENTS/Assignment_1/Data/subreddits.csv' -O subreddits -l /root/pg_assignment_1/opSubreddits.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -h 127.0.0.1

# TIME THE LOADING OF COMMENTS
pg_bulkload -i '/mnt/c/Amey/ASU/ASU_MCS/SPRING_23_CLASSES_SEM_2/CSE_511_DATA_PROCESSING_AT_SCALE/ASSIGNMENTS/Assignment_1/Data/comments.csv' -O comments -l /root/pg_assignment_1/opComments.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -h 127.0.0.1

# TIME THE LOADING OF SUBMISSIONS
pg_bulkload -i '/mnt/c/Amey/ASU/ASU_MCS/SPRING_23_CLASSES_SEM_2/CSE_511_DATA_PROCESSING_AT_SCALE/ASSIGNMENTS/Assignment_1/Data/submissions.csv' -O submissions -l /root/pg_assignment_1/opSubmissions.log -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -d postgres -h 127.0.0.1


