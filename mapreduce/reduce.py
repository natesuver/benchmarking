#!/usr/bin/env python
import sys
# maps words to their counts
word2count = {}
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        continue
    try:
        word2count[word] = word2count[word]+count
    except:
        word2count[word] = count
    # write the tuples to stdout

#Print list sorted by word count from lowest to highest
for w in sorted(word2count, key=word2count.get):
    print('%s\t%s'%(w, word2count[w]))

#for word in word2count.keys():
#   print('%s\t%s'%(word, word2count[word]))
