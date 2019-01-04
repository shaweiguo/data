#!/bin/sh
#py36=`source activate py36`
#echo py36
#hadoop=`start-all.sh`
#echo $hadoop

cd $SPARK_HOME
#spark=`sbin/start-all.sh`
#echo $spark
master=`sbin/start-master.sh`
echo $master
slave=`sbin/start-slave.sh spark://us:7077`
echo $slave

cd /home/sha/dev/ex/data
#python --version
PYSPARK_PYTHON=/home/sha/anaconda3/envs/p36/bin/python PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS="notebook" MASTER=spark://us:7077 pyspark --num-executors 1 --total-executor-cores 2 --executor-memory 512m
