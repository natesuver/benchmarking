#!/usr/bin/env python
import sys
import re
def main():
    #--- get all lines from stdin ---
    for line in sys.stdin:
        #--- remove leading and trailing whitespace---
        line = line.strip()
        #--- split the line into words ---
        words = line.split()
        #--- output tuples [word, 1] in tab-delimited format---
        for word in words:
            result=re.sub("[^A-Za-z|'|(-)]","", word) #remove any characters from the input that are not the letters a-z, single quote, or hyphen
            result=scrubSequence(word,"'") #scrub unnecessary quotes
            result=scrubSequence(word,"--") #scrub unnecessary double hyphens
            result=re.sub("(?<=[A-Za-z])-(?=[A-Za-z])", "",result) #remove any additional hyphens where the preceding character is a letter, and the subsequent character is also a letter.  This handles the case of single-hyphenated words that would not have been picked up with previous methods
            print('%s\t%s' %(result, "1")) #return the result standard out
      
#Given a target word, and sequence to operate against, does the following:
#Remove any instances of the target sequence that occur at the start of the word
#Remove any instances of the target sequence that occur at the end of the word
#Remove any instances of the target sequence where it occurs 2 or more times in succession
def scrubSequence(word, sequence):
    result=re.sub("^"+sequence,"", word)
    result=re.sub(sequence+"$","", result)
    result=re.sub(sequence+"{2,}","", result)
    return result

main()