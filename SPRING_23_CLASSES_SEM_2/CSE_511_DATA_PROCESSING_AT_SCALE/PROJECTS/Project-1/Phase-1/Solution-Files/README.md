
# Project 1 Group 10

You will find Zip File [here](https://github.com/CSE511-SPRING-2023/Project-1-Group-10/blob/main/%5BGroup-10%5D%5BProject1%5D%5BPhase1%5D.zip)
You will find Jar file [here](https://github.com/CSE511-SPRING-2023/Project-1-Group-10/blob/main/cse511/%5BGroup-10%5D%5BProject1%5D%5BPhase1%5D.jar)
## Run Project


To run this project locally, you need to run

```
docker run -it <Docker Image Name / Id>
```
- Once in the command prompt, to test the project, we have included a script file, automationTest.sh, which takes in a parameter 
```
    1 - rangequery
    2 - rangejoinquery
    3 - distancequery
    4 - distancejoinquery
    5 - All

    Example command to run rangequery would be
    sh automationTest.sh 1
```
- The script will take care of everything:
    - It will delete the current jar file if present.
    - It will delete any target folders present
    - It will then execute spark-submit job, depending on the parameter passed.
    - Then it will verify results with expected and current outputs.
    - Note this script will work only for test case which was provided in the problem description.

# We also have completed Bonus Assignment.

To run it, you can download the latest image or specific version of Image using following command.

```
    docker pull cnjarami/group10-project1-phase1-bonus:<Version Number>

Example Command:
    docker pull cnjarami/group10-project1-phase1-bonus:v0
    cd /root/cse511
```
You will find JAR file here, either you can run 

```
spark-submit CSE511-assembly-0.1.0.jar "result/output" "rangequery" "/root/cse511/src/resources/arealm10000.csv" "-93.63173,33.0183,-93.359203,33.219456" "rangejoinquery" "/root/cse511/src/resources/arealm10000.csv" "/root/cse511/src/resources/zcta10000.csv" "distancequery" "/root/cse511/src/resources/arealm10000.csv" "-88.331492,32.324142" "1" "distancejoinquery" "/root/cse511/src/resources/arealm10000.csv" "/root/cse511/src/resources/arealm10000.csv" "0.1"
```
Or, proceed with your testing part directly with code in the folder.

## Authors

- [@Amey Bhilegaonkar](https://ameyportfolio.netlify.app/)
- [@Gaurav Hoskote](https://github.com/gauravhoskote)
- [@Caleb Jaramillo](https://www.linkedin.com/in/caleb-jaramillo-167087226/)

## Support

For support, email 

    abhilega@asu.edu
    ghoskote@asu.edu
    cnjarami@asu.edu

- with the Subject: CSE511_DPS_PROJECT_QUERY, 
- with the Body: 
    - Name:
    - Query:
## 🔗 Links

- Amey Bhilegaonkar
    [![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ameyportfolio.netlify.app/)
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/amey-bhilegaonkar-942b70125/)

- Gaurav Hoskote
    [![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://gauravhoskote.github.io/)
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gauravhoskote/)

- Caleb Jaramillo
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/caleb-jaramillo-167087226/)
