import heapq
import queue
import time

import timer


class Ereignisliste:
    queue = []

    def __init__(self):
        heapq.heapify(self.queue)

    def pop(self):
        return heapq.heappop(self.queue)

    def push(self, a):
        heapq.heappush(self.queue, a)


class KundIn:
    list = []
    currentStation = ""
    currentT = 0
    currentW = 0
    currentN = 0
    startTime = 0
    endTime = 0

    def __init__(self, stationenTupleListe): #Liste aus Tuplen mit (Station, T, W, N)
        self.list = stationenTupleListe

    def beginn_einkauf(self):
        self.startTime = time.time()

    def ankunft_station(self):
        self.currentStation = self.list[0][0]
        self.currentT = self.list[0][1]
        self.currentW = self.list[0][2]
        self.currentN = self.list[0][3]

    def verlassen_station(self):
        self.list.pop[0]
        self.currentStation = ""
        self.currentT = 0
        self.currentW = 0
        self.currentN = 0


class Station:
    queue = []
    def __init__(self, bediendauer):
        self.Bediendauer = bediendauer

    def anstellen(self, KundIn): #Add to queue
        self.queue.append(KundIn)

    def fertig(self, KundIn): #Delete like FIFO
        self.queue.remove(self, KundIn)



a = Ereignisliste()
print(a.queue)
a.push(2)
print(a.queue)
print(a.pop())
print(a.queue)
