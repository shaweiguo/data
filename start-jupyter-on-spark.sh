#!/bin/sh

cd /home/sha/dev/ex/data
PYSPARK_PYTHON=/home/sha/anaconda3/envs/p36/bin/python PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS="notebook" MASTER=spark://us:7077 pyspark --driver-memory 512m --num-executors 2 --total-executor-cores 2 --executor-memory 1g
#--jars /opt/share/hbase/lib/hbase-client-2.1.0.jar,/opt/share/hbase/lib/hbase-common-2.1.0.jar,/opt/share/jdbc/mysql-connector-java-5.1.47-bin.jar,/opt/share/jdbc/postgresql-42.2.5.jar,/opt/share/hbase/lib/hbase-mapreduce-2.1.0.jar,/opt/share/hbase/lib/hbase-examples-2.1.0.jar,//opt/share/hbase/lib/hbase-*.jar

