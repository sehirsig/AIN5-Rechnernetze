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
STATION_FINISHED = 4

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
    maxEreignisnummer = 0
    ereignisnummer = 0
    uhr = None

    def __init__(self, s, e):
        self.maxSimulationsZeit = s
        self.maxEreignisnummer = e
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
                print("-----------------------")
                return;

            if (self.ereignisnummer == self.maxEreignisnummer):
                print("Ereignisnummer maximum reached.")
                print("-----------------------")
                return;

            d, e, f, g, caller = self.pop() #(ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)


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
    name = ""
    liste = list()
    curStation = 0 #(Station(Bediendauer), T, W, N)
    curBediendauer = 0
    curT = 0
    curW = 0
    curN = 0

    def __init__(self, stationenTupleListe, name):  # Liste aus Tuplen mit List((Station, T, W, N), (Station, T, W, N), ... )
        self.liste = list(stationenTupleListe)
        self.name = name


    def beginn_einkauf(self):  # Ereignis kreiren
        if self.liste:  # Wenn Liste nicht Leer ist
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)
            self.curBediendauer = self.curStation.bediendauer
            print(str(supermarkt.uhr.zeit) + "::  " "Kunde " + str(self.name) + " beginnt den Einkauf um " + str(supermarkt.uhr.zeit))
            print("Station: " + str(self.curStation.name)) # Abarbeitung, Eintrag in Eventliste wann nächste Ankunft
            print("T: " + str(self.curT)) # Zeit T die der Kunde benötigt um von Station y zu Station x zu kommen.
            print("W: " + str(self.curW)) # Ab welcher Wartenschlangenlänge W der Kunde die Station x auslässt
            print("N: " + str(self.curN)) # Anzahl der Einkäufe N, die Kunde an Station x tätigt.
            print("Bediendauer: " + str(self.curBediendauer))
            print("-----------------------")

            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.uhr.zeit + self.curT, supermarkt.ereignisnummer, 1, CUSTOMER_ARRIVE, self)
            supermarkt.push(neuesEreignis)

    def ankunft_station(self):  # Ereignis kreiren
        self.liste = self.liste  # Abarbeitung, Eintrag in Eventliste wann Zuende
        print(str(supermarkt.uhr.zeit) + "::  " + str(self.name) + " um " + str(supermarkt.uhr.zeit) + " an Station " + str(self.curStation.name) + " angekommen")
        print("-----------------------")
        #supermarkt.push(((supermarkt.uhr.zeit,2,supermarkt.ereignisnummer,CUSTOMER_ARRIVE,0), self)) # Debug/Test Push
        #supermarkt.ereignisnummer += 1
        # Stationsmethode aufrufen um anzustellen, oder wenn zuviel angestellt weiter springen
        if (len(self.curStation.queue) <= int(self.curW)): #überprüfen ob queue nicht zu lange
            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.uhr.zeit, supermarkt.ereignisnummer, 1, STATION_QUEUE, self)
            supermarkt.push(neuesEreignis)
        else:
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)
            self.curBediendauer = self.curStation.bediendauer
            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.uhr.zeit + self.curT, supermarkt.ereignisnummer, 1, CUSTOMER_ARRIVE, self)
            print(str(supermarkt.uhr.zeit) + "::  " + str(self.name) + " geht jetzt um " + str(
                supermarkt.uhr.zeit) + " zur Station " + str(self.curStation.name))
            print("-----------------------")
            supermarkt.push(neuesEreignis)#auslassen und nächste station ansteuern.

    def verlassen_station(self):  # Ereignis kreiren, Eintrag in Eventliste wann nächste Ankunft
        if (len(self.liste) == 0):
            print(str(supermarkt.uhr.zeit) + "::  " + str(self.name) + " um " + str(supermarkt.uhr.zeit) + " verlässt den Supermarkt.")
            print("-----------------------")
        else:
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)
            self.curBediendauer = self.curStation.bediendauer
            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.uhr.zeit + self.curT, supermarkt.ereignisnummer, 1, CUSTOMER_ARRIVE, self)
            print(str(supermarkt.uhr.zeit) + "::  " + str(self.name) + " geht jetzt um " + str(
                supermarkt.uhr.zeit) + " zur Station " + str(self.curStation.name))
            print("-----------------------")
            supermarkt.push(neuesEreignis)  # auslassen und nächste station ansteuern.

    def sagHallo(self):
        print(str(supermarkt.uhr.zeit) + "::  Ich bin ein Kunde " + str(self.name) + " um die Zeit " + str(supermarkt.uhr.zeit))
        print("-----------------------")



class Station:
    queue = list()
    bediendauer = 0
    name = ""

    def __init__(self, bediendauer, ereignisliste, name):
        self.bediendauer = bediendauer
        self.ereignisliste = ereignisliste
        self.name = name

    def anstellen(self, KundIn):  # Add to queue
        self.queue.append(KundIn)
        print(str(supermarkt.uhr.zeit) + "::  " + str(KundIn.name) + " stellt sich um " + str(supermarkt.uhr.zeit) + " bei " + str(self.name) + " als " + str(len(self.queue)) + " an.")
        print("-----------------------")
        supermarkt.ereignisnummer += 1
        neuesEreignis = (supermarkt.uhr.zeit + (self.bediendauer * int(KundIn.curN)), supermarkt.ereignisnummer, 1, STATION_FINISHED, KundIn)
        supermarkt.push(neuesEreignis)
        #Ereignis wann der Kunde bedient wird.

    def bedienen(self):
        aktuellerKunde = self.queue.pop()
        supermarkt.ereignisnummer += 1
        neuesEreignis = (supermarkt.uhr.zeit + self.bediendauer, supermarkt.ereignisnummer, 1, STATION_FINISHED, aktuellerKunde)
        supermarkt.push(neuesEreignis)

    def fertig(self, KundIn):
        # Abarbeitung
        self.queue.pop(0)
        print(str(supermarkt.uhr.zeit) + "::  " + str(KundIn.name) + " wurde um " + str(
            supermarkt.uhr.zeit) + " bei " + str(self.name) + " fertig bedient")
        print("-----------------------")
        KundIn.verlassen_station()




#Supermark initialisieren
maximalZeit = 347
maximalEreignis = 300
supermarkt = Ereignisliste(maximalZeit,maximalEreignis)

# Stationen
# Bäcker
baecker = Station(10, supermarkt, "Bäcker")
# Wursttheke
wursttheke = Station(30, supermarkt, "Wursttheke")
# Käsetheke
kaesetheke = Station(60, supermarkt, "Käsetheke")
# Kasse
kasse = Station(5, supermarkt, "Kasse")


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


def customerSpawner(maxZeit):
    abstandTyp1 = 200
    abstandTyp2 = 60
    startTyp1 = 0
    startTyp2= 1
    anzahlTyp1 = 0
    anzahlTyp2 = 0
    while ((int(startTyp1)) < int(maxZeit)):
        supermarkt.ereignisnummer += 1
        anzahlTyp1 += 1
        typ1Kunde = KundIn(typ1, f"Kunde {anzahlTyp1} Typ 1")
        # Ereignis = (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)
        # Ein Ereignis ist ein 5-Tupel
        neuesEreignis = (startTyp1, supermarkt.ereignisnummer, 3, CUSTOMER_ENTRANCE, typ1Kunde)
        startTyp1 += abstandTyp1
        supermarkt.push(neuesEreignis)

    while ((int(startTyp2)) < int(maxZeit)):
        supermarkt.ereignisnummer += 1
        anzahlTyp2 += 1
        typ2Kunde = KundIn(typ2, f"Kunde {anzahlTyp2} Typ 2")
        neuesEreignis = (startTyp2, supermarkt.ereignisnummer, 3, CUSTOMER_ENTRANCE, typ2Kunde)
        startTyp2 += abstandTyp2
        supermarkt.push(neuesEreignis)



if __name__ == '__main__':
    customerSpawner(maximalZeit)
    supermarkt.start()