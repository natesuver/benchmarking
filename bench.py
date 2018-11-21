'''
Script to perform simple floating point and integer benchmarking in python
@author: Nate Suver and Kam Larkins
'''
import threading
import datetime
import csv
import sys
import time


beginTest=False #a global flag we can use to tell all of the threads that we should begin testing
endTest=False #a global flag we can use to tell all of the threads that we should end testing
myInt=0

class Execution:
    minutes=0
    ops=0
    threadcount=0
    def __init__(self, minutes, ops, threadcount):
        self.ops=ops
        self.minutes=minutes
        self.threadcount=threadcount
    def toArray(self):
        return [self.minutes,self.ops,self.threadcount]

#write the results to a csv file we can import into excel
def writeResultToCsv(filename,executions):
    with open(filename, mode='w',newline='') as resultFile:
        writer = csv.writer(resultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in executions:
            writer.writerow(item.toArray())



def run(threadid):
    global myInt
    threadLock=threading.Lock()
    startTime = datetime.datetime.now()
    while not beginTest:
        print("Waiting on thread " + str(threadid) + " for test to begin")
    print("Test on thread " + str(threadid) + " has started!")
    while not endTest:
        threadLock.acquire()
        myInt+=1
        threadLock.release()
    endTime = datetime.datetime.now()
    print("Test complete on thread " + str(threadid) + ", ran for " + str(endTime-startTime) + " seconds" )

def executeTest(minutesToSleep):
    global beginTest
    global endTest
    beginTest = True
    time.sleep(minutesToSleep*60)
    endTest=True


def setupAndRunTest(minuteCount, threadsToRun):
    global myInt
    global beginTest
    global endTest
    threads=[]
    for i in range(threadsToRun):
        thr=threading.Thread(target=run, args=[i]) #TestRun()
        threads.append(thr)
        print("Start benchmarking on thread " + str(i) + " for " + str(minuteCount) + " minutes")
        thr.start()
        
    timerthread=threading.Thread(target=executeTest,args=[minuteCount])
    timerthread.start()
    for thread in threads:
        thread.join()
    result=myInt/(minuteCount*60) #compute number of computations per second
    print("Test run for " + str(minuteCount) + " minutes is complete, with a value of " + str(result) + " operations per second")
    result = Execution(minuteCount,result,threadsToRun)
    myInt=0 #reset our globals to prepare for the next test
    beginTest=False
    endTest=False
    return result

    #Start our benchmarks.  Arg 1 is the name of the file to write results to.  Arg2 are the number of threads to run.  Arg3 is the # of iterations per run
def main(filename, threadsToRun, iterations):
    executions=[]
    minuteCount=1
    while minuteCount<=iterations:
        result=setupAndRunTest(minuteCount,threadsToRun)
        executions.append(result)
        minuteCount+=1
    writeResultToCsv(filename,executions)

def getFile():
    filename = input("Enter the file you wish to save results to: ")
    return filename

def getThreads():
    while True:
        try:
            threads = int(input("Enter the number of threads: "))
            return int(threads)
        except ValueError:
            print("Error! Not a number!")
        else:
            break

def getRunNumber():
    while True:
        try:
            ints = int(input("Enter the number of test runs.  Each test run will run 1 minute longer than the last (e.g. entering '4' will run a test for 1 minute, 2 minutes, 3 minutes, and 4 minutes): "))
            return int(ints)
        except ValueError:
            print("Error! Not a number!")
        else:
            break
#filename = getFile()
#main(filename,threads,ints)
main('./results.csv',getThreads(),getRunNumber())