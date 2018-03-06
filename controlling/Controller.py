class Controller(object):

    def __init__(self, executor):
        self.executor = executor

    def switchToStart(self):
        print("hello world")
        self.executor.submit(print("switching to start now.."))

# States
#
# WaitForStart
## startsignalreceiver
# MoveToLoad
## movement
# GetLoad
## telescope
## positionoutput
## magnet
# SearchGoal
## movement
## positionoutput
# DeliverLoad
## telescope
## positionoutput
## magnet
# Finnish
## movement

