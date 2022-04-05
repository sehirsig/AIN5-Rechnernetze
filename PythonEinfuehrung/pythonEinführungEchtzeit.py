import time
from threading import Thread, Event
from queue import Queue

TIME_FACTOR = 1


class CustomerSpawner:
    def __init__(self):
        self.__t = Thread(target=self.__routine__)

    def __routine__(self):
        customer_id_type1 = 0
        customer_id_type2 = 0
        for i in range(400):
            print("Zeit: " + str(i))
            if (customer_id_type1 * 200) == i:
                print(f"Typ 1 Kunde {customer_id_type1 + 1} spawned at {i}")
                CustomerType1(customer_id_type1).start()
                customer_id_type1 += 1
            if ((customer_id_type2 * 60) + 1) == i:
                print(f"Typ 2 Kunde {customer_id_type2 + 1} spawned at {i}")
                CustomerType2(customer_id_type2).start()
                customer_id_type2 += 1
            time.sleep(1 * TIME_FACTOR)

    def start(self):
        self.__t.start()


class Customer:
    def __init__(self, customer_id, station_tuple_list):
        self.__t = Thread(target=self.__routine__)
        self.customer_id = customer_id
        self.beginServedEvt = Event()
        self.__number_of_items = 1
        self.station_tuple_list = station_tuple_list

    def start(self):
        self.__t.start()

    def __routine__(self):
        for e in self.station_tuple_list:
            STATION = e[0]
            QUEUE_LENGTH = e[2]
            WAY_TO_STATION = e[3]
            self.__number_of_items = e[3]

            time.sleep(WAY_TO_STATION)
            if STATION.queue_length() < QUEUE_LENGTH:
                STATION.enqueue(self)
                self.beginServedEvt.wait()
                STATION.endServeEvt.wait()
            else:
                print(self.description() + " lässt die Station " + STATION.description + "aus\n")
            print(self.description() + " ist fertig\n")

    def type(self):
        pass

    def description(self):
        return "Kunde " + str(self.type()) + "-" + str(self.customer_id)

    def getNumberOfItems(self):
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
            time.sleep(self.time_per_item * customer.getNumberOfItems())
            print(customer.description() + " verlässt " + self.description + "\n")
            self.endServeEvt.set()

    def start(self):
        self.__t.start()


stations = [Station("Bäcker", 10), Station("Wursttheke", 30), Station("Käsetheke", 60), Station("Kasse", 5)]

if __name__ == '__main__':
    for s in stations:
        s.start()

    customerSpawner = CustomerSpawner()
    customerSpawner.start()
