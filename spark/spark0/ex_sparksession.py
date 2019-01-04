import sys
sys.path.append('/home/sha/server/spark/')
from pyspark.sql import SparkSession

# spark = SparkSession.builder.master("local").appName("My Spark Application").config("spark.submit.deployMode", "client").getOrCreate()

# numlines = spark.sparkContext.textFile("file:///home/sha/sdk/spark/licenses").count()

# print("The total number of lines is " + str(numlines))

# df = spark.createDataFrame([
#     (1, 144.5, 5.9, 33, 'M'),
#     (2, 167.2, 5.4, 45, 'M'),
#     (3, 124.1, 5.2, 45, 'F'),
#     (4, 144.5, 5.9, 45, 'M'),
#     (5, 133.2, 5.7, 45, 'F'),
#     (3, 124.1, 5.2, 45, 'F'),
#     (5, 129.2, 5.3, 45, 'M'),
# ], ['id', 'weight', 'height', 'age', 'gender'])
#
# print('Count of rows: {0}'.format(df.count))
# print('Count of distinct rows: {0}'.format(df.distinct().count()))

logFile = "/home/sha/sdk/spark/README.md"  # Should be some file on your system
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()

print("************************Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()
