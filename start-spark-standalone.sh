#!/bin/sh
#p36=`source activate p36`
#echo p36

#cd $SPARK_HOME
#master=`sbin/start-master.sh`
#echo $master
#slave=`sbin/start-slave.sh spark://us:7077`
#echo $slave
spark=`$SPARK_HOME/sbin/start-all.sh`
echo $spark
