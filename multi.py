'''
Script to perform simple floating point and integer benchmarking in python
@author: Nate Suver and Kam Larkins
'''
import multiprocessing
import datetime
import csv
import sys
import time


beginTest=False #a global flag we can use to tell all of the processes that we should begin testing
endTest=False #a global flag we can use to tell all of the processes that we should end testing
myInt=0

class Execution:
    minutes=0
    ops=0
    processcount=0
    def __init__(self, minutes, ops, processcount):
        self.ops=ops
        self.minutes=minutes
        self.processcount=processcount
    def toArray(self):
        return [self.minutes,self.ops,self.processcount]

#write the results to a csv file we can import into excel
def writeResultToCsv(filename,executions):
    with open(filename, mode='w',newline='') as resultFile:
        writer = csv.writer(resultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in executions:
            writer.writerow(item.toArray())



def run(processid):
    global myInt
    processLock=multiprocessing.Lock()
    startTime = datetime.datetime.now()
    while not beginTest: #we use this first loop to help minimize the overhead of the processes starting.  All processes will be stuck in this same loop, until the timer process sets a global to break this loop, and they should all start at just about the same time.
        print("Waiting on process " + str(processid) + " for test to begin")
    print("Test on process " + str(processid) + " has started!")
    while not endTest:
        processLock.acquire()
        myInt+=1
        processLock.release()
    endTime = datetime.datetime.now()
    print("Test complete on process " + str(processid) + ", ran for " + str(endTime-startTime) + " seconds" )

def executeTest(minutesToSleep):
    global beginTest
    global endTest
    beginTest = True
    time.sleep(minutesToSleep*60)
    endTest=True


def setupAndRunTest(minuteCount, processesToRun):
    global myInt
    global beginTest
    global endTest
    processes=[]
    for i in range(processesToRun):
        thr=multiprocessing.Process(target=run, args=[i]) #TestRun()
        processes.append(thr)
        print("Start benchmarking on process " + str(i) + " for " + str(minuteCount) + " minutes")
        thr.start()
        
    timerprocess=multiprocessing.Process(target=executeTest,args=[minuteCount])
    timerprocess.start()
    for process in processes:
        process.join()
    result=round(myInt/(minuteCount*60)) #compute number of computations per second
    print("Test run for " + str(minuteCount) + " minutes is complete, with a value of " + str(result) + " operations per second")
    result = Execution(minuteCount,result,processesToRun)
    myInt=0 #reset our globals to prepare for the next test
    beginTest=False
    endTest=False
    return result

#Start our benchmarks.  Arg 1 is the name of the file to write results to.  Arg2 are the number of processes to run.  Arg3 is the # of iterations per run.  Each iteration will run one minute longer than the last.
def main(filename, processesToRun, iterations):
    executions=[]
    minuteCount=1
    while minuteCount<=iterations:
        result=setupAndRunTest(minuteCount,processesToRun)
        executions.append(result)
        minuteCount+=1
    writeResultToCsv(filename,executions)

def getFile():
    filename = input("Enter the file you wish to save results to: ")
    return filename

def getprocesses():
    try:
        processes = int(input("Enter the number of processes: "))
        return int(processes)
    except ValueError:
        print("Error! Not a number!")

def getRunNumber():
    try:
        ints = int(input("Enter the number of test runs.  Each test run will run 1 minute longer than the last (e.g. entering '4' will run a test for 1 minute, 2 minutes, 3 minutes, and 4 minutes): "))
        return int(ints)
    except ValueError:
        print("Error! Not a number!")

#filename = getFile()
#main(filename,processes,ints)
main('./results.csv',2,2) #