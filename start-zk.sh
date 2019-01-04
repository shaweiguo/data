#!/bin/sh
cd $KAFKA_HOME

zookeeper=`bin/zookeeper-server-start.sh config/zookeeper.properties`
echo $zookeeper

kafka=`bin/kafka-server-start.sh config/server.properties`
echo $kafka

topic=`bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test`
echo $topic

list_topic=`bin/kafka-topics.sh --list --zookeeper localhost:2181`
echo $list_topic

produce=`bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test`
echo $produce

##consume=`bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning`
##echo $consume
