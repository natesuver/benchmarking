'''
Script to perform simple floating point and integer benchmarking in python
@author: Nate Suver and Kam Larkins
'''
import threading
import time
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

class benchInteger(threading.Thread):
    executions=[]
    def __init__(self, threadId):
        threading.Thread.__init__(self)
        self.threadId=threadId
    def run(self):
        #here we will run some nice code to compute things
        print("Start benchmarking")
        start=time.time()
        end=time.time()
        return execution(0,0,1)

threads=[]

for i in range(int(sys.argv[2])):
    thr=benchInteger(i)
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
