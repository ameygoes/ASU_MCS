import pyarrow.parquet as pq

# Read the parquet file
table = pq.read_table('yellow_tripdata_2022-03.parquet')

# Select the first 50 rows using slicing
head1 = table[:50]
head2 = table[51:100]
head3 = table[101:150]

# Write the selected rows to a new parquet file
pq.write_table(head1, 'test1.parquet')
pq.write_table(head2, 'test2.parquet')
pq.write_table(head3, 'test3.parquet')

