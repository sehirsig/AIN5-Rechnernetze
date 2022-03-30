import heapq
from threading import Lock

#Idee
# Nur Kunden rufen die Ereignisliste auf, neue Ereignisse.
# Die Stationen bekommen wir aus der Liste des Kunden, und können von da deren Methoden aufrufen


time = 0
ereignisnummer = 0

queuePushLock = Lock()
queuePopLock = Lock()

# Konstanten für Ereignisse
CUSTOMER_ENTRANCE = 0
CUSTOMER_ARRIVE = 1
CUSTOMER_EXIT = 2
STATION_QUEUE = 3
STATION_SERVE = 4
STATION_FINISHED = 5

#Tupel (Kunde,ZeitpunktVerlassen,letzteStation)
kunde_zwischen_stationen = []


class Ereignisliste:
    simulationszeit = 0
    ereignisnummer = 0

    def __init__(self, s, e):
        self.simulationszeit = s
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
        while not self.isEmpty():
            tuple, caller = self.pop()
            d, e, f, g, h = tuple #(ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)
            if (isinstance(caller, KundIn)): # Wenn der Aufrufer ein KundIn ist. Muss immer Kunde sein, sonnst klappt heapQueue nicht!
                caller.sagHallo()
                #TESTEN, welche Ereignisfunktion
                if g == CUSTOMER_ENTRANCE:
                    caller.beginn_einkauf()
                elif g == CUSTOMER_ARRIVE:
                    caller.ankunft_station()
                elif g == CUSTOMER_EXIT:
                    caller.verlassen_station()
                elif g == STATION_QUEUE:
                    station_temp = caller.liste[0][0]
                    station_temp.anstellen(caller)
                elif g == STATION_SERVE:
                    station_temp = caller.liste[0][0]
                    station_temp.bedienen()
                elif g == STATION_FINISHED:
                    station_temp = caller.liste[0][0]
                    station_temp.fertig(caller)
                else:
                    rr = 2 #Just a Blank, nothing for use

                #print(caller)
                #print(d)
                #print(e)
                #print(f)
                #print(g)
                #print(h)
        # Simulationszeit schreitet voran
        ereignisListe.simulationszeit+=1


class KundIn:
    liste = list()

    def __init__(self, stationenTupleListe):  # Liste aus Tuplen mit List((Station, T, W, N), (Station, T, W, N), ... )
        self.liste = list(stationenTupleListe)
        self.aufenthalt = None
        self.bedientBis = None

    def beginn_einkauf(self):  # Ereignis kreiren
        if self.liste:  # Wenn Liste nicht Leer ist
            self.liste = self.liste  # Abarbeitung, Eintrag in Eventliste wann nächste Ankunft

    def ankunft_station(self):  # Ereignis kreiren
        self.liste = self.liste  # Abarbeitung, Eintrag in Eventliste wann Zuende
        ereignisListe.push(((4,4,4,4,4), self)) # Debug/Test Push
        # Stationsmethode aufrufen um anzustellen, oder wenn zuviel angestellt weiter springen (liste pop)

    def verlassen_station(self):  # Ereignis kreiren, Eintrag in Eventliste wann nächste Ankunft
        self.liste.pop()

    def sagHallo(self):
        print("Ich bin ein Kunde")

    def einkaufen(self): pass

    def wechseln(self): pass

    def einkauf_beendet(self):
        ereignisListe.simulationszeit == self.bedientBis


class KundeTyp1(KundIn):
    def __init__(self, stationenTupleListe):
        KundIn.__init__(stationenTupleListe)

    def einkaufen(self):
        print()

    def wechseln(self):
        print()


class KundeTyp2(KundIn):
    def __init__(self, stationenTupleListe):
        KundIn.__init__(stationenTupleListe)

    def einkaufen(self):
        print()

    def wechseln(self):
        print()


#Station Status
STATION_IDLE = 0
STATION_BUSY = 1

class Station:
    station_status = STATION_IDLE
    queue = list()
    Bediendauer = 0

    def __init__(self, bediendauer, ereignisliste):
        self.Bediendauer = bediendauer
        self.aktuellerKunde = None
        self.bedient_seit = 0
        self.ereignisliste = ereignisliste

    def anstellen(self, KundIn):  # Add to queue
        self.queue.append(KundIn)
        #Ereignis wann der Kunde bedient wird.

    def bedienen(self):
        self.aktuellerKunde = self.queue.pop()
        self.station_status = STATION_BUSY

    def fertig(self, KundIn):  # Delete like FIFO
        # Abarbeitung
        global time
        self.ereignisliste.push((time, 0, 0, 0, 0))
        if (self.isEmpty()):
            self.station_status = STATION_IDLE

    def isEmpty(self):
        return len(self.queue) == 0

    def istFertig(self):
        return self.aktuellerKunde.einkaufBeendet()


ereignisListe = Ereignisliste(150, 0)
# Stationen
# Bäcker
baecker = Station(10, ereignisListe)
# Wursttheke
wursttheke = Station(30, ereignisListe)
# Käsetheke
kaesetheke = Station(60, ereignisListe)
# Kasse
kasse = Station(5, ereignisListe)


# Typ 1 (Station(Bediendauer), T, W, N)
# Bäcker (baecker, 10, 10, 10)
# Wursttheke (wursttheke, 30, 10, 5)
# Käsetheke (kaesetheke, 45, 5, 3)
# Kasse (kasse, 60, 20, 30)
typ1 = list(((baecker, 10, 10, 10), (wursttheke, 30, 10, 5), (kaesetheke, 45, 5, 3), (kasse, 60, 20, 30)))

# Typ 2 (Station(Bediendauer), T, W, N)
# Wursttheke (wursttheke, 30, 5, 2)
# Kasse (kasse, 30, 20, 3)
# Bäcker (baecker, 20, 20, 3)
typ2 = list(((wursttheke, 30, 5, 2), (kasse, 30, 20, 3), (baecker, 20, 20, 3)))

typ1kunde1 = KundIn(typ1)
typ2kunde1 = KundIn(typ2)

# Ereignis = (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)
# Ein Ereignis ist ein 5-Tupel
ereignis1 = ((1, 2, 3, 1, 5), typ1kunde1)
ereignis2 = ((2, 2, 3, 2, 5), typ1kunde1)
ereignis3 = ((6, 7, 8, 9, 10), typ2kunde1)

a = Ereignisliste(20, 20)

a.push(ereignis1)
a.push(ereignis2)
a.push(ereignis3)

a.start()
