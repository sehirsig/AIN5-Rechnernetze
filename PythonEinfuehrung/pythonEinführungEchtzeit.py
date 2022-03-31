import heapq
import time
from threading import Thread, Lock, Event
from queue import Queue


def spawn_customers():
    customer_id_type1 = 0
    customer_id_type2 = 0
    while True:
        time.sleep(1)
        CustomerType1(customer_id_type1).start()
        customer_id_type1 += 1
        time.sleep(1)
        CustomerType2(customer_id_type2).start()
        customer_id_type2 += 1


class Customer:
    def __init__(self, customer_id):
        self.__t = Thread(target=self.__routine__)
        self.customer_id = customer_id

    def start(self):
        self.__t.start()

    def __routine__(self):
        pass

    def type(self):
        pass


class CustomerType1(Customer):
    def __init__(self, customer_id):
        Customer.__init__(self, customer_id)

    def __routine__(self):
        time.sleep(5)
        stations[0].enqueue(self)

    def type(self):
        return 1


class CustomerType2(Customer):
    def __init__(self, customer_id):
        Customer.__init__(self, customer_id)

    def __routine__(self):
        time.sleep(10)
        stations[1].enqueue(self)

    def type(self):
        return 2


class Station:
    def __init__(self, description):
        self.description = description
        self.__current_customer__ = None
        self.__customer_queue__ = Queue()
        self.startServeEvt = Event()
        self.endServeEvt = Event()

    def enqueue(self, customer):
        self.__customer_queue__.put(customer)
        s = "Kunde " + str(customer.type()) + "-" + str(customer.customer_id) + " bei " + self.description + " eingereiht!"
        print(s)

    def dequeue(self):
        return self.__customer_queue__.get()

    def queue_length(self):
        return len(self.__customer_queue__)


stations = [Station("Bäcker"), Station("Wursttheke"), Station("Käsetheke"), Station("Kasse")]

if __name__ == '__main__':
    q = Queue()
    customerSpawner = Thread(target=spawn_customers)
    customerSpawner.start()
