import heapq

# Konstanten für Ereignisse
CUSTOMER_ENTRANCE = 0
CUSTOMER_ARRIVE = 1
STATION_QUEUE = 2
STATION_FINISHED = 3


class Ereignisliste:
    maxSimulationsZeit = 0
    maxEreignisnummer = 0
    ereignisnummer = 0

    def __init__(self, s, e):
        self.maxSimulationsZeit = s
        self.maxEreignisnummer = e
        self.queue = []

    def pop(self):
        e = heapq.heappop(self.queue)
        return e

    def push(self, a):
        heapq.heappush(self.queue, a)

    def isEmpty(self):
        return len(self.queue) == 0

    def start(self):  # Startet die Simulation
        self.zeit = 0
        while not self.isEmpty():

            if (self.ereignisnummer == self.maxEreignisnummer): #Wenn die vorgegebene Ereignisnummer erreicht ist, abbrechen.
                print("Ereignisnummer maximum reached.")
                print("-----------------------")
                print("Rest:")
                while not self.isEmpty():
                    popped = self.pop()
                    #Die noch verbliebenen Events per print zeigen.
                    print(popped)
                statistikAuswerten()
                return;

            d, e, f, g, caller = self.pop()  # (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)

            if (self.zeit != d):
                while d > self.zeit:
                    self.zeit += 1

            if (isinstance(caller,
                           KundIn)):  # Wenn der Aufrufer ein KundIn ist. Muss immer Kunde sein, sonnst klappt heapQueue nicht!
                if g == CUSTOMER_ENTRANCE:
                    caller.beginn_einkauf()
                elif g == CUSTOMER_ARRIVE:
                    caller.ankunft_station()
                elif g == STATION_QUEUE:
                    station_temp = caller.curStation
                    station_temp.anstellen(caller)
                elif g == STATION_FINISHED:
                    station_temp = caller.curStation
                    station_temp.fertig(caller)
                    caller.verlassen_station()

            if (self.isEmpty()): # Wenn Eventliste fertig ist, alles auswerten.
                statistikAuswerten()
                return;


class KundIn:
    name = ""
    liste = list()
    curStation = None
    curT = 0
    curW = 0
    curN = 0

    # Statistiken
    kompletteEinkaufszeit = 0
    uebersprungeneStationen = 0

    def __init__(self, stationenTupleListe,
                 name):  # Liste aus Tuplen mit List((Station, T, W, N), (Station, T, W, N), ... )
        self.liste = list(stationenTupleListe)
        self.name = name

    def beginn_einkauf(self):  # Ereignis kreiren
        if self.liste:  # Wenn Liste nicht Leer ist
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)
            self.kompletteEinkaufszeit = supermarkt.zeit

            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.zeit + self.curT, 3, supermarkt.ereignisnummer, CUSTOMER_ARRIVE, self)
            supermarkt.push(neuesEreignis)

    def ankunft_station(self):
        #Statistik
        self.curStation.anzahlDerKunden += 1

        # überprüfen ob queue nicht zu lange, false => überspringen
        if len(self.curStation.queue) + 1 <= int(self.curW):
            #Neues Event, welches angibt, dass der Kunde sich jetzt sofort in die Queue einreiht.
            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.zeit, 1, supermarkt.ereignisnummer, STATION_QUEUE, self)
            supermarkt.push(neuesEreignis)

            # Statistik und LOG
            output_customer.append(f"{supermarkt.zeit}:{self.name} Queueing at {self.curStation.name}")
        else:
            # Wenn Queue zu lange, überspringen und die nächste Station ansteuern

            #Statistik und LOG
            self.curStation.anzahlAusgelassen += 1
            self.uebersprungeneStationen += 1
            output_customer.append(f"{supermarkt.zeit}:{self.name} Dropped at {self.curStation.name}")

            # Wenn alle Stationen besucht sind, den Supermarkt verlassen. Die Zeit stoppen, um die Einkaufszeit festzuhalten.
            if len(self.liste) == 0:
                self.kompletteEinkaufszeit = supermarkt.zeit - self.kompletteEinkaufszeit
                return;

            #Neue Station holen
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)

            #Neues Ereignis, wann der Kunde bei der Station ankommt
            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.zeit + self.curT, 3, supermarkt.ereignisnummer, CUSTOMER_ARRIVE, self)
            supermarkt.push(neuesEreignis)

    def verlassen_station(self):
        output_customer.append(f"{supermarkt.zeit}:{self.name} Finished at {self.curStation.name}")
        if (len(self.liste) == 0):
            # Wenn alle Stationen besucht sind, den Supermarkt verlassen. Die Zeit stoppen, um die Einkaufszeit festzuhalten.
            self.kompletteEinkaufszeit = supermarkt.zeit - self.kompletteEinkaufszeit
        else:
            self.curStation, self.curT, self.curW, self.curN = self.liste.pop(0)

            #Neues Event, wann der Kunde an diese nächste Station ankommen wird.
            supermarkt.ereignisnummer += 1
            neuesEreignis = (supermarkt.zeit + self.curT, 3, supermarkt.ereignisnummer, CUSTOMER_ARRIVE, self)
            supermarkt.push(neuesEreignis)

#Station Status
NOTBUSY = 0
BUSY = 1

class Station:
    queue = list()
    bediendauer = 0
    name = ""
    status = 0

    # Statistik
    anzahlAusgelassen = 0
    anzahlDerKunden = 0

    def __init__(self, bediendauer, name):
        self.bediendauer = bediendauer
        self.name = name
        self.queue = list()
        self.status = NOTBUSY

    def isEmpty(self):
        return len(self.queue) == 0

    def anstellen(self, KundIn):
        #In der Queue einreihen
        self.queue.append(KundIn)

        #LOG
        output_station.append(f"{supermarkt.zeit}:{self.name} adding customer {KundIn.name}")

        if self.status == NOTBUSY:
            #LOG
            output_station.append(f"{supermarkt.zeit}:{self.name} serving customer {KundIn.name}")

            #Status auf BUSY setzen
            self.status = BUSY

            # Ereignis wann der Kunde bedient wird.
            supermarkt.ereignisnummer += 1
            neuesEreignis = (
            supermarkt.zeit + (self.bediendauer * int(KundIn.curN)), 2, supermarkt.ereignisnummer, STATION_FINISHED,
            KundIn)
            supermarkt.push(neuesEreignis)

    def fertig(self, KundIn):
        # Variable customer initialisieren
        customer = KundIn
        # Wenn die Liste nicht leer ist, den Kunden nach FIFO-Policy poppen
        if not self.isEmpty():
            customer = self.queue.pop(0)

        #Status auf NOTBUSY stellen
        self.status = NOTBUSY

        #LOG
        output_station.append(f"{supermarkt.zeit}:{self.name} finished customer {KundIn.name}")

        #Wenn die Kiste nicht leer ist und der gepopte Kunde nicht derselbe vom Parameter ist, weitergehen.
        if not self.isEmpty() or customer != KundIn:
            # Wenn der custommer der Kunde aus dem Parameter ist, neu poppen.
            if customer == KundIn:
                customer = self.queue.pop(0)

            #Status auf Busy setzen
            self.status = BUSY

            #Statistik
            output_station.append(f"{supermarkt.zeit}:{self.name} serving customer {customer.name}")

            #Neues Ereignis, welches angibt wann der Kunde fertig bedient wurde.
            supermarkt.ereignisnummer += 1
            neuesEreignis = (
            supermarkt.zeit + (self.bediendauer * int(customer.curN)), 2, supermarkt.ereignisnummer, STATION_FINISHED,
            customer)
            supermarkt.push(neuesEreignis)


# Supermark initialisieren
maximalZeit = 1800
maximalEreignis = 1000000
supermarkt = Ereignisliste(maximalZeit, maximalEreignis)

# Stationen
# Bäcker
baecker = Station(10, "Bäcker")
# Wursttheke
wursttheke = Station(30, "Metzger")
# Käsetheke
kaesetheke = Station(60, "Käse")
# Kasse
kasse = Station(5, "Kasse")

#
## Typ 1 (Station(Bediendauer), T, W, N)
## Bäcker (baecker, 10, 10, 10)
## Wursttheke (wursttheke, 30, 10, 5)
## Käsetheke (kaesetheke, 45, 5, 3)
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

# Statistiken
liste_aller_kunden = list()


def getKundenAnzahl():
    return len(liste_aller_kunden)

#Listen für Customer/Station Output
output_customer = list()
output_station = list()


def customerSpawner(maxZeit):
    abstandTyp1 = 200
    abstandTyp2 = 60
    startTyp1 = 0
    startTyp2 = 1
    anzahlTyp1 = 0
    anzahlTyp2 = 0

    #Event für Kunden vom Typ 1 festlegen.
    while ((int(startTyp1)) <= int(maxZeit)):
        supermarkt.ereignisnummer += 1
        anzahlTyp1 += 1
        typ1Kunde = KundIn(typ1, f"A{anzahlTyp1}")
        # Ereignis = (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargument)
        # Ein Ereignis ist ein 5-Tupel
        neuesEreignis = (startTyp1, supermarkt.ereignisnummer, 1, CUSTOMER_ENTRANCE, typ1Kunde)
        startTyp1 += abstandTyp1
        supermarkt.push(neuesEreignis)
        liste_aller_kunden.append(typ1Kunde)

    #Event für Kunden vom Typ 2 festlegen.
    while ((int(startTyp2)) <= int(maxZeit)):
        supermarkt.ereignisnummer += 1
        anzahlTyp2 += 1
        typ2Kunde = KundIn(typ2, f"B{anzahlTyp2}")
        neuesEreignis = (startTyp2, supermarkt.ereignisnummer, 1, CUSTOMER_ENTRANCE, typ2Kunde)
        startTyp2 += abstandTyp2
        supermarkt.push(neuesEreignis)
        liste_aller_kunden.append(typ2Kunde)


def statistikAuswerten():

    #supermarkt_customer Output
    for output in output_customer:
        print(output)

    #supermarkt_station Output
    for output in output_station:
        print(output)

    anzahl_vollstaendiger_einkaufe = 0
    liste_aller_kunden.sort(key=lambda x: x.kompletteEinkaufszeit)

    mittlere_einkaufsdauer = 0
    mittlere_einkaufsdauer_vollstaendig = 0

    for customer in liste_aller_kunden:
        if (customer.uebersprungeneStationen == 0):
            anzahl_vollstaendiger_einkaufe += 1
            mittlere_einkaufsdauer_vollstaendig = mittlere_einkaufsdauer_vollstaendig + customer.kompletteEinkaufszeit
        mittlere_einkaufsdauer = mittlere_einkaufsdauer + customer.kompletteEinkaufszeit

    mittlere_einkaufsdauer = mittlere_einkaufsdauer / getKundenAnzahl()
    mittlere_einkaufsdauer_vollstaendig = mittlere_einkaufsdauer_vollstaendig / anzahl_vollstaendiger_einkaufe

    droppercentageBaecker = baecker.anzahlAusgelassen * 100 /baecker.anzahlDerKunden if baecker.anzahlAusgelassen != 0 else 0
    droppercentageWursttheke = wursttheke.anzahlAusgelassen * 100 / wursttheke.anzahlDerKunden if wursttheke.anzahlAusgelassen != 0 else 0
    droppercentageKaesetheke = kaesetheke.anzahlAusgelassen * 100 / kaesetheke.anzahlDerKunden if kaesetheke.anzahlAusgelassen != 0 else 0
    droppercentageKasse = kasse.anzahlAusgelassen * 100 / kasse.anzahlDerKunden if kasse.anzahlAusgelassen != 0 else 0

    print(f"\nSimulationsende: {supermarkt.zeit}s")
    print(f"Anzahl Kunden: {len(liste_aller_kunden)}")
    print(f"Anzahl vollständige Einkäufe: {anzahl_vollstaendiger_einkaufe}")
    print(f"Mittlere Einkaufsdauer: %.2fs" % mittlere_einkaufsdauer)
    print(f"Mittlere Einkaufsdauer (vollständig): %.2fs" % mittlere_einkaufsdauer_vollstaendig)
    print(f"Drop percentage at Bäcker: %.2f" % droppercentageBaecker)
    print(f"Drop percentage at Wursttheke: %.2f" % droppercentageWursttheke)
    print(f"Drop percentage at Käsetheke: %.2f" % droppercentageKaesetheke)
    print(f"Drop percentage at Kasse: %.2f" % droppercentageKasse)

if __name__ == '__main__':
    customerSpawner(maximalZeit)
    supermarkt.start()
