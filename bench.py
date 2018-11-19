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
    def __init__(self, threadId, executionsPerRun):
        threading.Thread.__init__(self)
        self.threadId=threadId
        self.executionsPerRun=executionsPerRun
    def run(self):
        #here we will run some nice code to compute things
        print("Start benchmarking thread " + str(self.threadId))
        for runNumber in range(25): #for each test, we will run 25 passes.
            codeToExec='''
i=0
i=i+1'''
            computationTime=timeit.timeit(stmt=codeToExec,number=self.executionsPerRun)
            compsPerSecond=self.executionsPerRun/computationTime #divide to get computations per second
            self.executions.append(execution(compsPerSecond,runNumber,self.threadId))

#write the results to a csv file we can import into excel
def writeResultToCsv(filename,threads):
    with open(filename, mode='w',newline='') as resultFile:
        writer = csv.writer(resultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for thread in threads:
            for item in thread.executions:
                writer.writerow(item.toArray())

#Start our benchmarks.  Arg 1 is the name of the file to write results to.  Arg2 are the number of threads to run.  Arg3 is the # of iterations per run
def main(filename, threadsToRun, executionsPerRun):

    threads=[]
    for i in range(threadsToRun):
        thr=bench(i,executionsPerRun)
        threads.append(thr)
        thr.start()
    for thread in threads:
        thread.join()
    writeResultToCsv(filename,threads)

main("./results.csv",int(3),int(1000000))