#!/bin/sh
cd /home/sha/ex/data/lib/Data_Analytics_with_Spark_Using_Python
SPARK_EXECUTOR_MEMORY=512m spark-submit --master spark://us:7077 wordcounts.py /opt/data/txt/shakespeare.txt /opt/data/txt/wordcounts^C

