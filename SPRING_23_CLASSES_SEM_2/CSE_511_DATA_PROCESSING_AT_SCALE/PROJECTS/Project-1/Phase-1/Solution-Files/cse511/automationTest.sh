cd /root/cse511

rm CSE511-assembly-0.1.0.jar
rm -rf result
rm -rf spark-warehouse
sbt assembly

cp target/scala-2.11/CSE511-assembly-0.1.0.jar /root/cse511/CSE511-assembly-0.1.0.jar

rm -rf target
rm -rf /root/cse511/project/target

if [ $1 = 1 ]
then
   spark-submit CSE511-assembly-0.1.0.jar "result/output" "rangequery" "/root/cse511/src/resources/arealm10000.csv" "-93.63173,33.0183,-93.359203,33.219456"
   
   count=$(head result/output0/*01*.csv)
   
	if [ $count = 4 ]
	then
		echo "Test Case: RangeQuery Passed"
	else
		echo "Test Case: RangeQuery Failed"
	fi
   
   
elif [ $1 = 2 ] 
then
spark-submit CSE511-assembly-0.1.0.jar "result/output" "rangejoinquery" "/root/cse511/src/resources/arealm10000.csv" "/root/cse511/src/resources/zcta10000.csv"

	count=$(head result/output0/*01*.csv)
   
	if [ $count = 7612 ]
	then
		echo "Test Case: Range-Join-Query Passed"
	else
		echo "Test Case: Range-Join-Query Failed"
	fi

elif [ $1 = 3 ] 
then
spark-submit CSE511-assembly-0.1.0.jar "result/output" "distancequery" "/root/cse511/src/resources/arealm10000.csv" "-88.331492,32.324142" "1"

	count=$(head result/output0/*01*.csv)
   
	if [ $count = 302 ]
	then
		echo "Test Case: Distanceq-Query Passed"
	else
		echo "Test Case: Distanceq-Query Failed"
	fi

elif [ $1 = 4 ] 
then
spark-submit CSE511-assembly-0.1.0.jar "result/output" "distancejoinquery" "/root/cse511/src/resources/arealm10000.csv" "/root/cse511/src/resources/arealm10000.csv" "0.1"

	count=$(head result/output0/*01*.csv)
   
	if [ $count = 123362 ]
	then
		echo "Test Case: Range-Query Passed"
	else
		echo "Test Case: Range-Query Failed"
	fi

else
   spark-submit CSE511-assembly-0.1.0.jar "result/output" "rangequery" "/root/cse511/src/resources/arealm10000.csv" "-93.63173,33.0183,-93.359203,33.219456" "rangejoinquery" "/root/cse511/src/resources/arealm10000.csv" "/root/cse511/src/resources/zcta10000.csv" "distancequery" "/root/cse511/src/resources/arealm10000.csv" "-88.331492,32.324142" "1" "distancejoinquery" "/root/cse511/src/resources/arealm10000.csv" "/root/cse511/src/resources/arealm10000.csv" "0.1"

   count0=$(head result/output0/*art-00001*.csv)
   count1=$(head result/output1/*art-00001*.csv)
   count2=$(head result/output2/*art-00001*.csv)
   count3=$(head result/output3/*art-00001*.csv)
   
   	if [ $count0 = 4 ] && [ $count1 = 7612 ] && [ $count2 = 302 ] && [ $count3 = 123362 ]
	then
		echo "Test Cases: All Passed"
	else
		echo "Test Cases: All Failed"
	fi

fi
