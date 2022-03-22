import heapq
from threading import Lock

# Ereignis = (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)
# Ein Ereignis ist ein 5-Tupel
ereignis1 = (0, 0, 0, 0, 0)
ereignis2 = (1, 0, 0, 0, 0)
ereignis3 = (2, 0, 0, 0, 0)

queuePushLock = Lock()
queuePopLock = Lock()

class Ereignisliste:
    queue = []
    simulationszeit = 0
    ereignisnummer = 0

    def __init__(self, s, e):
        self.simulationszeit = s
        self.ereignisnummer = e

    def pop(self):
        queuePopLock.acquire()
        e = heapq.heappop(self.queue)
        queuePopLock.release()
        return e

    def push(self, a):
        queuePushLock.acquire()
        heapq.heappush(self.queue, a)
        queuePushLock.release()

    def start(self):  # Startet die Simulation
        for event in self.queue:
            # Do Something with Event
            print(event)
            self.queue.pop


class KundIn:
    liste = list()

    def __init__(self, stationenTupleListe):  # Liste aus Tuplen mit List((Station, T, W, N), (Station, T, W, N), ... )
        self.liste = list(stationenTupleListe)

    def beginn_einkauf(self): #Ereignis kreiren
        if self.liste: #Wenn Liste nicht Leer ist
            self.liste = self.liste# Abarbeitung

    def ankunft_station(self): #Ereignis kreiren
        self.liste = self.liste# Abarbeitung

    def verlassen_station(self): #Ereignis kreiren
        self.liste.pop()



class Station:
    queue = list()
    Bediendauer = 0

    def __init__(self, bediendauer):
        self.Bediendauer = bediendauer

    def anstellen(self, KundIn):  # Add to queue
        self.queue.append(KundIn)

    def fertig(self, KundIn):  # Delete like FIFO
        # Abarbeitung
        self.queue.remove(self, KundIn)


# Stationen
# Bäcker
baecker = Station(10)
# Wursttheke
wursttheke = Station(30)
# Käsetheke
kaesetheke = Station(60)
# Kasse
kasse = Station(5)

# Typ 1 (Station(Bediendauer), T, W, N)
# Bäcker (baecker, 10, 10, 10)
# Wursttheke (wursttheke, 30, 10, 5)
# Käsetheke (kaesetheke, 45, 5, 3)
# Kasse (kasse, 60, 20, 30)
typ1 = list(((baecker,10, 10, 10), (wursttheke,30, 10, 5), (kaesetheke,45, 5, 3), (kasse,60, 20, 30)))

# Typ 2 (Station(Bediendauer), T, W, N)
# Wursttheke (wursttheke, 30, 5, 2)
# Kasse (kasse, 30, 20, 3)
# Bäcker (baecker, 20, 20, 3)
typ2 = list(((wursttheke,30, 5, 2), (kasse,30, 20, 3), (baecker,20, 20, 3)))

print(typ1)

a = Ereignisliste(20, 20)

a.push(ereignis1)
a.push(ereignis2)
a.push(ereignis3)

a.start()
