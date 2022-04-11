import time
from threading import Thread, Event
from queue import Queue

TIME_FACTOR = 0.1 # 0.5 => Doppelt so schnell

END_TIME = 0
MAX_TIME = 1800

class CustomerSpawner:
    def __init__(self):
        self.__t = Thread(target=self.__routine__)

    def __routine__(self):
        customer_id_type1 = 0
        customer_id_type2 = 0
        for i in range(2147483647):
            TIME = i
            if (i <= MAX_TIME):
                print("Zeit: " + str(i) + "\n")
                if (customer_id_type1 * 200) == i:
                    c = CustomerType1(customer_id_type1)
                    liste_aller_kunden.append(c)
                    customer_id_type1 += 1
                    c.start()
                    print(str(TIME) + ":" + c.description() + " betritt den Supermarkt\n")
                if ((customer_id_type2 * 60) + 1) == i:
                    c = CustomerType2(customer_id_type2)
                    liste_aller_kunden.append(c)
                    customer_id_type2 += 1
                    c.start()
                    print(str(TIME) + ":" + c.description() + " betritt den Supermarkt\n")
            else:
                not_all_finish_flag = 0
                for customers in liste_aller_kunden:
                    if customers.buy_status == NOT_FINISHED:
                        not_all_finish_flag = 1
                        break;
                if not not_all_finish_flag:
                    END_TIME = i
                    statistikAuswerten()
                    return
            time.sleep(1 * TIME_FACTOR)

    def start(self):
        self.__t.start()


#CUSTOMER Variables
NOT_FINISHED = False
FINISHED = True

class Customer:
    def __init__(self, customer_id, station_tuple_list):
        self.__t = Thread(target=self.__routine__)
        self.customer_id = customer_id
        self.beginServedEvt = Event()
        self.__number_of_items = 1
        self.station_tuple_list = station_tuple_list
        #Statistik
        self.buy_status = NOT_FINISHED
        self.kompletteEinkaufszeit = time.time()
        self.uebersprungeneStationen = 0

    def start(self):
        self.__t.start()

    def __routine__(self):
        #time.sleep(0.4 * TIME_FACTOR) #To be within the second
        for e in self.station_tuple_list:
            STATION = e[0]
            WAY_TO_STATION = e[1]
            QUEUE_LENGTH = e[2]
            self.__number_of_items = e[3]

            STATION.anzahlDerKunden += 1

            time.sleep(WAY_TO_STATION * TIME_FACTOR)
            if STATION.queue_length() < QUEUE_LENGTH:
                STATION.enqueue(self)
                self.beginServedEvt.wait()
                STATION.endServeEvt.wait()
            else:
                print(self.description() + " lässt die Station " + STATION.description + "aus")
                STATION.anzahlAusgelassen += 1
                self.uebersprungeneStationen += 1
            print(self.description() + " ist fertig")
        print(self.description() + "verlässt den Supermarkt")
        self.buy_status = FINISHED
        self.kompletteEinkaufszeit = (time.time() - self.kompletteEinkaufszeit) * TIME_FACTOR

    def type(self):
        pass

    def description(self):
        return "Kunde " + str(self.type()) + "-" + str(self.customer_id)

    def get_number_of_items(self):
        return self.__number_of_items


# tuple: (station, way to station, may queue length, number of items)

class CustomerType1(Customer):
    def __init__(self, customer_id):
        Customer.__init__(self, customer_id,
                          [(stations[0], 10, 10, 10), (stations[1], 30, 10, 5), (stations[2], 45, 5, 3), (stations[3], 60, 20, 30)])

    def type(self):
        return 1


class CustomerType2(Customer):
    def __init__(self, customer_id):
        Customer.__init__(self, customer_id,
                          [(stations[1], 30, 5, 2), (stations[3], 30, 20, 3), (stations[0], 20, 20, 3)])

    def type(self):
        return 2


class Station:
    def __init__(self, description, time_per_item):
        self.description = description
        self.__current_customer__ = None
        self.__customer_queue__ = Queue()
        self.enqueue_Evt = Event()
        self.endServeEvt = Event()
        self.__t = Thread(target=self.__routine__)
        self.time_per_item = time_per_item
        self.anzahlAusgelassen = 0
        self.anzahlDerKunden = 0

    def enqueue(self, customer):
        self.__customer_queue__.put(customer)
        self.enqueue_Evt.set()
        print(customer.description() + " bei " + self.description + " eingereiht; Warteschlange: "
              + str(self.__customer_queue__.qsize()) + "\n")

    def dequeue(self):
        customer = self.__customer_queue__.get()
        customer.beginServedEvt.set()
        return customer

    def queue_length(self):
        return self.__customer_queue__.qsize()

    def queue_is_empty(self):
        return self.__customer_queue__.empty()

    def __routine__(self):
        while True:
            self.enqueue_Evt.clear()
            while self.queue_is_empty():
                self.enqueue_Evt.wait()
            customer = self.dequeue()
            print(customer.description() + " wird bei " + self.description + " bedient\n")
            time.sleep(self.time_per_item * customer.get_number_of_items() * TIME_FACTOR)
            print(customer.description() + " verlässt " + self.description + "\n")
            self.endServeEvt.set()

    def start(self):
        self.__t.start()


stations = [Station("Bäcker", 10), Station("Wursttheke", 30), Station("Käsetheke", 60), Station("Kasse", 5)]


#Statistik
liste_aller_kunden = list()

def getKundenAnzahl():
    return len(liste_aller_kunden)

#Listen für Customer/Station Output
output_customer = list()
output_station = list()

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

    droppercentageBaecker = stations[0].anzahlAusgelassen * 100 /stations[0].anzahlDerKunden if stations[0].anzahlAusgelassen != 0 else 0
    droppercentageWursttheke = stations[1].anzahlAusgelassen * 100 / stations[1].anzahlDerKunden if stations[1].anzahlAusgelassen != 0 else 0
    droppercentageKaesetheke = stations[2].anzahlAusgelassen * 100 / stations[2].anzahlDerKunden if stations[2].anzahlAusgelassen != 0 else 0
    droppercentageKasse = stations[3].anzahlAusgelassen * 100 / stations[3].anzahlDerKunden if stations[3].anzahlAusgelassen != 0 else 0

    #print(f"\nSimulationsende: {supermarkt.zeit}s")
    #print(f"\nSimulationsende: xs")
    print(f"Anzahl Kunden: {len(liste_aller_kunden)}")
    print(f"Anzahl vollständige Einkäufe: {anzahl_vollstaendiger_einkaufe}")
    print(f"Mittlere Einkaufsdauer: %.2fs" % mittlere_einkaufsdauer)
    print(f"Mittlere Einkaufsdauer (vollständig): %.2fs" % mittlere_einkaufsdauer_vollstaendig)
    print(f"Drop percentage at Bäcker: %.2f" % droppercentageBaecker)
    print(f"Drop percentage at Wursttheke: %.2f" % droppercentageWursttheke)
    print(f"Drop percentage at Käsetheke: %.2f" % droppercentageKaesetheke)
    print(f"Drop percentage at Kasse: %.2f" % droppercentageKasse)

if __name__ == '__main__':
    for s in stations:
        s.start()

    customerSpawner = CustomerSpawner()
    customerSpawner.start()
