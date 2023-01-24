#
# sample_csv.ctl -- Control file to load CSV input data
#
#    Copyright (c) 2007-2023, NIPPON TELEGRAPH AND TELEPHONE CORPORATION
#
OUTPUT = postgres.submissions                   # [<schema_name>.]table_name
INPUT = /mnt/c/Amey/ASU/ASU_MCS/SPRING_23_CLASSES_SEM_2/CSE_511_DATA_PROCESSING_AT_SCALE/ASSIGNMENTS/Assignment_1/Data/submissions.csv  # Input data location (absolute path)
TYPE = CSV                            # Input file type
QUOTE = "\""                          # Quoting character
ESCAPE = \                            # Escape character for Quoting
DELIMITER = ","                       # Delimiter
