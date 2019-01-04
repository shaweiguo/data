#!/bin/sh
#py36=`source deactivate`
#echo py36
#cd $SPARK_HOME
#spark=`sbin/stop-all.sh`
#echo spark
#slave=`sbin/stop-slave.sh`
#echo $slave
#master=`sbin/stop-master.sh`
#echo $master

spark=`$SPARK_HOME/sbin/stop-all.sh`
echo $spark

#hadoop=`stop-all.sh`
#echo hadoop
#PYSPARK_PYTHON=/home/sha/anaconda3/envs/py36/bin/python PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS="notebook" MASTER=spark://us:7077 pyspark --num-executors 1 --total-executor-cores 2 --executor-memory 512m
#cd /home/sha/dev/ex/data
