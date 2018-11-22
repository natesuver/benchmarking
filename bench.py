'''
Script to perform simple floating point and integer benchmarking in python
@author: Nate Suver and Kam Larkins
'''
import threading
import datetime
import csv
import sys
import time

class Execution:
    minutes=0
    ops=0
    threadcount=0
    passCount=0
    def __init__(self, minutes, ops, threadcount):
        self.ops=ops
        self.minutes=minutes
        self.threadcount=threadcount
    def toArray(self):
        return [self.minutes,self.ops,self.threadcount, self.passCount]

class Benchmark:
    beginTest = False #a flag we can use to tell all of the threads that we should begin testing
    endTest = False #a flag we can use to tell all of the threads that we should end testing
    opCounter = 0 #a variable we use to perform counting

    def __init__(self,minuteCount, threadsToRun,useFloat):
        self.minuteCount = minuteCount
        self.threadsToRun = threadsToRun
        self.useFloat = useFloat

    def count(self, threadid):
        threadLock=threading.Lock()
        startTime = datetime.datetime.now()
        if (self.useFloat==True):
            increment=1.0
        else:
            increment=1
        while not self.beginTest: #we use this first loop to help minimize the overhead of the threads starting.  All threads will be stuck in this same loop, until the timer thread sets a global to break this loop, and they should all start at just about the same time.
            print("Waiting on thread " + str(threadid) + " for test to begin")
        print("Test on thread " + str(threadid) + " has started!")
        while not self.endTest:
            threadLock.acquire()
            self.opCounter+=increment
            threadLock.release()
        endTime = datetime.datetime.now()
        print("Test complete on thread " + str(threadid) + ", ran for " + str(endTime-startTime) + " seconds" )

    def beginCounting(self,minutesToSleep):
        self.beginTest = True
        time.sleep(minutesToSleep*60)
        self.endTest=True

    #begin the test.
    def start(self):
        global opCounter
        self.reset(self.useFloat)
        threads=[]
        for i in range(self.threadsToRun):
            thr=threading.Thread(target=self.count, args=[i]) #TestRun()
            threads.append(thr)
            print("Start benchmarking on thread " + str(i) + " for " + str(self.minuteCount) + " minutes")
            thr.start()
            
        timerthread=threading.Thread(target=self.beginCounting,args=[self.minuteCount])
        timerthread.start()
        for thread in threads:
            thread.join()
        result=round(self.opCounter/(self.minuteCount*60)) #compute number of computations per second
        print("Test run for " + str(self.minuteCount) + " minutes is complete, with a value of " + str(result) + " operations per second")
        result = Execution(self.minuteCount,result,self.threadsToRun)
        return result

    #reset our class variables to prepare for the next test
    def reset(self,useFloat):
        if (useFloat==True):
            self.opCounter=0.0
        else:
            self.opCounter=0
        self.beginTest=False
        self.endTest=False

#Start our benchmarks.  Arg 1 is the name of the file to write results to.  Arg2 are the number of threads to run.  Arg3 is the # of iterations per run.  Each iteration will run one minute longer than the last.
def main(filename, iterations, useFloat):
    executions=[]
    for passCount in [1,2,3]: #each test needs to be run 3 times
        for threadsToRun in [1,2,4,8]: #each test needs to be repeated with either 1,2,4,8 threads
            minuteCount=1
            while minuteCount<=iterations:
                bench = Benchmark(minuteCount,threadsToRun,useFloat)
                result=bench.start()
                result.passCount=passCount
                executions.append(result)
                minuteCount+=1
    writeResultToCsv(filename,executions)

#write the results to a csv file we can import into excel
def writeResultToCsv(filename,executions):
    with open(filename, mode='w',newline='') as resultFile:
        writer = csv.writer(resultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in executions:
            writer.writerow(item.toArray())



def getFile():
    filename = input("Enter the file you wish to save results to: ")
    return filename

def getCountingType():
    try:
        countType = int(input("Enter 1 to count integers, or 2 to count floats: "))
        if countType==2:
            return True
        return False
    except ValueError:
        print("Error! Not a number!")
    else:
        pass

def getRunNumber():
    try:
        ints = int(input("Enter the number of test runs.  Each test run will run 1 minute longer than the last \n (e.g. entering '4' will run a test for 1 minute, 2 minutes, 3 minutes, and 4 minutes): "))
        return int(ints)
    except ValueError:
        print("Error! Not a number!")
    else:
        pass

main('./results.csv',getRunNumber(),getCountingType())