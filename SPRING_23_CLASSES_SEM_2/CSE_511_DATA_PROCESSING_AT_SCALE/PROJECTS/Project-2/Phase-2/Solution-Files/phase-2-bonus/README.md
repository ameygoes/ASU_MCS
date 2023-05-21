
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

# start minikube
minikube start --driver=docker --alsologtostderr

# check minikube status
minikube status

# Enable Kubernetes in Docker Desktop and Switch to correct context
kubectl config use-context <context_name>

# To check existing pods and their status
kubectl get pods

# Create kafka pod with kafka-setup.yaml and zookeeper-setup.yaml
kubectl apply -f zookeeper-setup.yaml
kubectl apply -f kafka-setup.yaml
kubectl get pods

# Open two terminals 

## Terminal 1 
kubectl exec -it kafka-deployment-795fd84678-mg46x -- sh

## Terminal 2
kubectl exec -it kafka-deployment-795fd84678-mg46x -- sh

## Terminal 1 
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
kafka-console-producer --bootstrap-server localhost:9092 --topic test

## Terminal 2
kafka-console-consumer --bootstrap-server localhost:9092 --topic test

## Terminal 1
Hi I am Amey

## Terminal 2 
You should see that message- Hi I am Amey

# Now come back to the main terminal and Check if no errors in below command for zookeeper 
kubectl logs zookeeper-deployment-7bd58d655c-nxqcx