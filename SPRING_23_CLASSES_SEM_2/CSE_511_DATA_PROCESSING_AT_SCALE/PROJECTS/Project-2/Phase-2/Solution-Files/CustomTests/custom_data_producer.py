# Some parts of the file may need to be modified to suit your environment
from confluent_kafka import Producer
import pyarrow.parquet as pq
import time
import pandas as pd

# set the topic name
topic_name = "nyc_taxicab_data"
conf = {'bootstrap.servers': 'localhost:9092'}

# create a Kafka producer instance
producer = Producer(conf)

# Check if the producer is connected to Kafka
print(producer.list_topics().topics)
print("-----------------------------")

for i in range(1,4):
    # load the Parquet dataset
    trips = pq.read_table(f'parquetFiles/test{i}.parquet')
    trips = trips.to_pandas()

    # iterate over each row in the table and send it to Kafka
    for index, row in trips.iterrows():

        # select a subset of columns
        row = row[['trip_distance', 'PULocationID', 'DOLocationID', 'fare_amount']]

        # convert the row to a JSON string
        row = row.to_json()
        
        # encode the row as bytes
        message = str(row).encode('utf-8')

        # send the message to Kafka
        producer.produce(topic_name, value=message)
        producer.flush()

        # print
        print("Message sent to Kafka: {}".format(message))

        # wait for 0.25 seconds
        time.sleep(1)

    print(f"File test{i}.parquet was successfully loaded.")
# close the producer connection
producer.close()
