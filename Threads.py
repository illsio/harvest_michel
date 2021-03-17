import threading, time
from database.database import saveAlertEntry, loadJSON, countAll, fetchAll

class Threads:
    WAIT_TIME_SECONDS = 2
    #WAIT_TIME_SECONDS = 86400

    def __init__(self):
        self.ticker = None
        self.WAIT_TIME_SECONDS = 2

    def startThread(self):
        print("Hello World!")
        print("Current entries" + str(countAll()))
        # data = loadJSON()
        # saveAlertEntry(data)
        self.ticker = threading.Event()
        while not self.ticker.wait(self.WAIT_TIME_SECONDS):
            self.foo()

    ##Threading
    def foo(self):
        print("saving entries started")
        print(time.ctime())
        #data = loadJSON()
        #saveAlertEntry(data)