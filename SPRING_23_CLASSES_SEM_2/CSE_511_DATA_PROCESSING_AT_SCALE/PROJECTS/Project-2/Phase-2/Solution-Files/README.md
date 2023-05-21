
# CSE 511 Data Processing at Scale - Project-Phase-2-Bonus

![alt text](https://github.com/ameygoes/ASU_MCS/blob/master/SPRING_23_CLASSES_SEM_2/CSE_511_DATA_PROCESSING_AT_SCALE/ASSIGNMENTS/Assignment_1/images/spark.png)



## 🚀 About Me
🔭 I’m currently a Computer Science Graduate Student at Arizona State University.

🌱 Visit my [PortFolio](https://ameyportfolio.netlify.app/)

👯 I’m looking for Summer Internship Opportunities to expand my knowledge and network.

👨‍💻 All of my projects are available at my [GitHub](https://github.com/ameygoes)

📫 How to reach me amey.bhilegaonkar@asu.edu




## Authors

- [@Amey Bhilegaonkar](https://ameyportfolio.netlify.app/)
 

# Commands to run and deploy the Services

#### start minikube
```minikube start --driver=docker --cpus=4 --memory=5933```
#### check minikube status
```minikube status```
#### Enable Kubernetes in Docker Desktop and Switch to correct context

```kubectl config use-context <context_name>```

#### To check existing pods and their status
```kubectl get pods```

#### Create kafka pod with kafka-setup.yaml and zookeeper-setup.yaml
```
kubectl apply -f zookeeper-setup.yaml
kubectl apply -f kafka-setup.yaml
helm install my-neo4j-release neo4j/neo4j -f neo4j-values.yaml
kubectl apply -f neo4j-service.yaml
kubectl apply -f kafka-neo4j-connector.yaml
```
# Open two terminals 

#### Terminal 1 
```kubectl port-forward svc/neo4j-service 7474:7474 7687:7687```

#### Terminal 2
```kubectl port-forward svc/kafka-service 9092:9092```

Now here I added my custom test cases, for testing to run with three cases run following command.
Directory Structure of CustomTests looks like this:
-parquetFiles
    - parquet.py - File to create multiple parquet files from original one, as it is too big for low machine laptops
    - custom_tester.py - Tests file against custom tests
    - custom_data_producer.py - Adds data to Neo4J
#### Terminal 3 - To Run Custom Tests
```
cd CustomTests\
python custom_data_producer.py
python custom_tester.py
```


#### Terminal 4 - To Run tests given by CSE-511 class TA
```
python3 data_producer.py
python3 tester.py
```