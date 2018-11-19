'''
Script to perform simple floating point and integer benchmarking in python
@author: Nate Suver and Kam Larkins
'''
import threading
import timeit
import csv
import sys

class execution:
    runNumber=0
    computations=0
    threadNum=0
    def __init__(self, runNumber, computations, threadNum):
        self.computations=computations
        self.runNumber=runNumber
        self.threadNum=threadNum
    def toArray(self):
        return [self.runNumber,self.computations,self.threadNum]

class bench(threading.Thread):
    executions=[]
    def __init__(self, threadId):
        threading.Thread.__init__(self)
        self.threadId=threadId
    def run(self):
        #here we will run some nice code to compute things
        print("Start benchmarking thread " + self.threadId)
        elapsed=timeit.timeit(self.calcInt)
        return execution(100000,elapsed,self.threadId)

    def calcInt(self):
        r=0
        for i in range(100000):
            r=r+1


threads=[]

for i in range(int(sys.argv[2])):
    thr=bench(i)
    threads.append(thr)
    thr.start()

def writeResultToCsv(argv):
    with open(argv[1], mode='w') as resultFile:
        writer = csv.writer(resultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for thread in threads:
            for execution in thread.executions:
                writer.writerow(execution)

for thread in threads:
    thread.join()

writeResultToCsv(sys.argv)
