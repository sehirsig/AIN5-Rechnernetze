import heapq
from threading import Lock, Thread
import time

#Idee
# Nur Kunden rufen die Ereignisliste auf, neue Ereignisse.
# Die Stationen bekommen wir aus der Liste des Kunden, und können von da deren Methoden aufrufen


queuePushLock = Lock()
queuePopLock = Lock()


# Konstanten für Ereignisse
CUSTOMER_ENTRANCE = 0
CUSTOMER_ARRIVE = 1
CUSTOMER_EXIT = 2
STATION_QUEUE = 3
STATION_SERVE = 4
STATION_FINISHED = 5

zeitSkalierung = 0.2 # 1 = normal -> 0.5 doppelt so schnell

class timer:
    def __init__(self):
        self.__t = Thread(target=self.__routine__)

    zeit = 0
    def __routine__(self):
        while (self.zeit < supermarkt.maxSimulationsZeit):
            time.sleep(1 * zeitSkalierung)
            self.zeit = self.zeit + 1

    def start(self):
        self.__t.start()

class Ereignisliste:
    maxSimulationsZeit = 0
    ereignisnummer = 0
    uhr = None

    def __init__(self, s, e):
        self.maxSimulationsZeit = s
        self.ereignisnummer = e
        self.queue = []

    def pop(self):
        queuePopLock.acquire()
        e = heapq.heappop(self.queue)
        queuePopLock.release()
        return e

    def push(self, a):
        queuePushLock.acquire()
        heapq.heappush(self.queue, a)
        queuePushLock.release()

    def isEmpty(self):
        return len(self.queue) == 0

    def start(self):  # Startet die Simulation
        self.uhr = timer()
        self.uhr.start()
        while not self.isEmpty():

            if (self.uhr.zeit == self.maxSimulationsZeit): # Wenn maximale Simulationszeit erreicht, beenden.
                print("Time over.")
                return;

            tuple, caller = self.pop()
            d, e, f, g, h = tuple #(ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)


            if (self.uhr.zeit != d):
                while d > self.uhr.zeit:
                    if (self.uhr.zeit == self.maxSimulationsZeit):  # Wenn maximale Simulationszeit erreicht, beenden.
                        return;
                    time.sleep(0.45 * zeitSkalierung)

            if (isinstance(caller, KundIn)): # Wenn der Aufrufer ein KundIn ist. Muss immer Kunde sein, sonnst klappt heapQueue nicht!
                #caller.sagHallo()
                #TESTEN, welche Ereignisfunktion
                if g == CUSTOMER_ENTRANCE:
                    caller.beginn_einkauf()
                elif g == CUSTOMER_ARRIVE:
                    caller.ankunft_station()
                elif g == CUSTOMER_EXIT:
                    caller.verlassen_station()
                elif g == STATION_QUEUE:
                    station_temp = caller.curStation
                    station_temp.anstellen(caller)
                elif g == STATION_SERVE:
                    station_temp = caller.curStation
                    station_temp.bedienen()
                elif g == STATION_FINISHED:
                    station_temp = caller.curStation
                    station_temp.fertig(caller)

                #print(caller)
                #print(d)
                #print(e)
                #print(f)
                #print(g)
                #print(h)


class KundIn:
    liste = list()
    curStation = 0 #(Station(Bediendauer), T, W, N)
    curBediendauer = 0
    curT = 0
    curW = 0
    curN = 0

    def __init__(self, stationenTupleListe):  # Liste aus Tuplen mit List((Station, T, W, N), (Station, T, W, N), ... )
        self.liste = list(stationenTupleListe)


    def beginn_einkauf(self):  # Ereignis kreiren
        if self.liste:  # Wenn Liste nicht Leer ist
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)
            self.curBediendauer = self.curStation.Bediendauer
            print(str(supermarkt.uhr.zeit) + "::  " "Kunde " + str(self) + " beginnt den Einkauf um " + str(supermarkt.uhr.zeit))
            print("Station: " + str(self.curStation)) # Abarbeitung, Eintrag in Eventliste wann nächste Ankunft
            print("T: " + str(self.curT)) # Zeit T die der Kunde benötigt um von Station y zu Station x zu kommen.
            print("W: " + str(self.curW)) # Ab welcher Wartenschlangenlänge W der Kunde die Station x auslässt
            print("N: " + str(self.curN)) # Anzahl der Einkäufe N, die Kunde an Station x tätigt.
            print("Bediendauer: " + str(self.curBediendauer))
            print("-----------------------")

            supermarkt.ereignisnummer += 1
            neuesEreignis = ((supermarkt.uhr.zeit + self.curT, supermarkt.ereignisnummer, 1, CUSTOMER_ARRIVE, 5), self)
            supermarkt.push(neuesEreignis)

    def ankunft_station(self):  # Ereignis kreiren
        self.liste = self.liste  # Abarbeitung, Eintrag in Eventliste wann Zuende
        print(str(supermarkt.uhr.zeit) + "::  " + str(self) + "um " + str(supermarkt.uhr.zeit) + " an Station " + str(Station) + " angekommen")
        print("-----------------------")
        #supermarkt.push(((supermarkt.uhr.zeit,2,supermarkt.ereignisnummer,CUSTOMER_ARRIVE,0), self)) # Debug/Test Push
        #supermarkt.ereignisnummer += 1
        # Stationsmethode aufrufen um anzustellen, oder wenn zuviel angestellt weiter springen
        if (len(self.curStation.queue) <= int(self.curW)): #überprüfen ob queue nicht zu lange
            supermarkt.ereignisnummer += 1
            neuesEreignis = ((supermarkt.uhr.zeit, supermarkt.ereignisnummer, 1, STATION_QUEUE, self.curN), self)
            supermarkt.push(neuesEreignis)
        else:
            pass#auslassen und nächste station ansteuern. TODO

    def verlassen_station(self):  # Ereignis kreiren, Eintrag in Eventliste wann nächste Ankunft
        #self.liste.pop()
        pass

    def sagHallo(self):
        print(str(supermarkt.uhr.zeit) + "::  Ich bin ein Kunde " + str(self) + " um die Zeit " + str(supermarkt.uhr.zeit))

    def einkaufen(self): pass

    def wechseln(self): pass

    def einkauf_beendet(self):
        supermarkt.zeit == self.bedientBis


class Station:
    queue = list()
    Bediendauer = 0

    def __init__(self, bediendauer, ereignisliste):
        self.Bediendauer = bediendauer
        self.aktuellerKunde = None
        self.bedient_seit = 0
        self.ereignisliste = ereignisliste

    def anstellen(self, KundIn):  # Add to queue
        self.queue.append(KundIn)
        print(str(supermarkt.uhr.zeit) + "::  " + str(KundIn) + " stellt sich um " + str(supermarkt.uhr.zeit) + " bei " + str(self) + " als " + str(len(self.queue)) + " an.")
        print("-----------------------")
        #Ereignis wann der Kunde bedient wird.

    def bedienen(self):
        self.aktuellerKunde = self.queue.pop()

    def fertig(self, KundIn):  # Delete like FIFO
        # Abarbeitung
        global time
        self.ereignisliste.push((time, 0, 0, 0, 0))

    def isEmpty(self):
        return len(self.queue) == 0

    def getQueueLength(self):
        return len(self.queue)

    def istFertig(self):
        return self.aktuellerKunde.einkaufBeendet()



#Supermark initialisieren
supermarkt = Ereignisliste(120,20)

# Stationen
# Bäcker
baecker = Station(10, supermarkt)
# Wursttheke
wursttheke = Station(30, supermarkt)
# Käsetheke
kaesetheke = Station(60, supermarkt)
# Kasse
kasse = Station(5, supermarkt)


# Typ 1 (Station(Bediendauer), T, W, N)
# Bäcker (baecker, 10, 10, 10)
# Wursttheke (wursttheke, 30, 10, 5)
# Käsetheke (kaesetheke, 45, 5, 3)
# Kasse (kasse, 60, 20, 30)
typ1 = list()
typ1.append((baecker, 10, 10, 10))
typ1.append((wursttheke, 30, 10, 5))
typ1.append((kaesetheke, 45, 5, 3))
typ1.append((kasse, 60, 20, 30))

# Typ 2 (Station(Bediendauer), T, W, N)
# Wursttheke (wursttheke, 30, 5, 2)
# Kasse (kasse, 30, 20, 3)
# Bäcker (baecker, 20, 20, 3)
typ2 = list()
typ2.append((wursttheke, 30, 5, 2))
typ2.append((kasse, 30, 20, 3))
typ2.append((baecker, 20, 20, 3))

typ1kunde1 = KundIn(typ1)
typ2kunde1 = KundIn(typ2)
typ1kunde2 = KundIn(typ1)
typ2kunde2 = KundIn(typ2)

# Ereignis = (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)
# Ein Ereignis ist ein 5-Tupel
ereignis1 = ((0, 3, 1, CUSTOMER_ENTRANCE, 5), typ1kunde1)
ereignis2 = ((30, 3, 2, CUSTOMER_ENTRANCE, 5), typ1kunde2)
ereignis3 = ((1, 3, 3, CUSTOMER_ENTRANCE, 10), typ2kunde1)
ereignis4 = ((61, 3, 4, CUSTOMER_ENTRANCE, 10), typ2kunde2)


if __name__ == '__main__':
    supermarkt.push(ereignis3)
    supermarkt.push(ereignis4)
    supermarkt.push(ereignis1)
    supermarkt.push(ereignis2)
    supermarkt.ereignisnummer = 4
    supermarkt.start()


