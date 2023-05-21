# Grading Env-ish

This file will give a very brief overview of what steps will be performed by the grading environment to give you a better idea of how the test cases will be run.

> We will have some things installed and in the PATH variable already. Keep an eye out for those.
> Multiple terminals are to be used at certain places in this code file

## Startup

We already have minikube in the machine and the grading script will perform the following steps:

> These commands are run in the same or different terminal instances as required

```bash
minikube start <additional settings>
```

## Step 1

Here we will test your deployment of Zookeeper and Kafka. We will run the following commands:

```bash
kubectl apply -f ./zookeeper-setup.yaml
kubectl apply -f ./kafka-setup.yaml
```

## Step 2

Here we will test your deployment of Neo4j:

> helm is already installed in the setup and the neo4j helm chart available

```bash
helm install my-neo4j-release neo4j/neo4j -f neo4j-values.yaml
kubectl apply -f neo4j-service.yaml
```

## Step 3

The penultimate step is to test your deployment of the Kafka-Neo4j connection. We will run the following commands:

```bash
kubectl apply -f kakfa-neo4j-connector.yaml
```

## Step 4

The final step is to test your deployment of the entire pipeline with the interface file. We will run the following commands:

> There are hidden test cases that are present at every step

```bash
kubectl port-forward svc/neo4j-service 7474:7474 7687:7687
kubectl port-forward svc/kafka-service 9092:9092
python3 data_producer.py
python3 tester.py
```
