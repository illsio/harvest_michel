import threading, time
from database.database import saveAlertEntry, loadJSON, countAll, fetchAll

class Threads:
    #WAIT_TIME_SECONDS = 2
    #WAIT_TIME_SECONDS = 20
    WAIT_TIME_SECONDS = 86400
    COUNTER_THREAD = 'counter'

    def __init__(self):
        self.ticker = None

    def startThread(self):
        isCounter = False

        for thread in threading.enumerate():
            if thread.name is self.COUNTER_THREAD:
                isCounter = True
                break
        if isCounter:
            print("there is an existing counter thread")
            return "there is an existing counter thread"
        else:
            print("no existing counter thread - starting ...")
            ticker = threading.Thread(target=self.never_stop, name=self.COUNTER_THREAD, args=(self.WAIT_TIME_SECONDS,))
            ticker.start()
            return "no existing counter thread - starting ..."

    def never_stop(self, x):
        counter = threading.Event()
        while not counter.wait(x):
            self.startSavingThread()

    ##Threading
    def startSavingThread(self):
        entriesBefore = str(countAll())
        print("saving entries started at: ")
        print(time.ctime())
        data = loadJSON()
        saveAlertEntry(data)
        entriesAfter = str(countAll())
        print("we had: " + entriesBefore + " entries now we have: " + entriesAfter + " entries")
