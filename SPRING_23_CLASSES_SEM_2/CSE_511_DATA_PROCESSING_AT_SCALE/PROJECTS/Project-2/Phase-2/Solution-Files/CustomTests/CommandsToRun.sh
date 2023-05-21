# docker pull veedata/kafka-neo4j-connect
# minikube start --driver=docker --alsologtostderr --cpus=4 --memory=6000

kubectl apply -f ./zookeeper-setup.yaml
kubectl apply -f ./kafka-setup.yaml
helm install my-neo4j-release neo4j/neo4j -f neo4j-values.yaml
kubectl apply -f neo4j-service.yaml
kubectl apply -f kakfa-neo4j-connector.yaml
kubectl port-forward svc/neo4j-service 7474:7474 7687:7687
kubectl port-forward svc/kafka-service 9092:9092
python3 data_producer.py
python3 tester.py