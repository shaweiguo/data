import sys, re
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName('Word Counts')
sc = SparkContext(conf=conf)

if (len(sys.argv) != 3):
    print('''Usage: wordcounts.py <input_file_or_dir> <output_dir>''')
    sys.exit(0)
else:
    input_path = sys.argv[1]
    output_dir = sys.argv[2]


word_counts = sc.textFile('file://' + input_path) \
                .filter(lambda line: len(line) > 0) \
                .flatMap(lambda line: re.split('\W+', line)) \
                .filter(lambda word: len(word) > 0) \
                .map(lambda word: (word.lower(), 1)) \
                .reduceByKey(lambda v1, v2: v1 + v2) \
                .map(lambda x: (x[1], x[0])) \
                .sortByKey(ascending=False) \
                .persist()
word_counts.saveAsTextFile('file://' + output_dir)
top5_words = word_counts.take(5)
just_words = []
for wc in top5_words:
    just_words.append(wc[1])

print('The top 5 words are:')
print(str(just_words))
print('Check the complete outpue in ' + output_dir)