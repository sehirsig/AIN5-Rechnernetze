import time
from threading import Thread, Event
from queue import Queue


class CustomerSpawner:
    def __init__(self):
        self.__t = Thread(target=self.__routine__)

    def __routine__(self):
        customer_id_type1 = 0
        customer_id_type2 = 0
        for i in range(400):
            print("Zeit: " + str(i))
            if ((customer_id_type1 * 200) == i):
                print(f"Typ 1 Kunde {customer_id_type1 + 1} spawned at {i}")
                CustomerType1(customer_id_type1).start()
                customer_id_type1 += 1
            if (((customer_id_type2 * 60) + 1) == i):
                print(f"Typ 2 Kunde {customer_id_type2 + 1} spawned at {i}")
                CustomerType2(customer_id_type2).start()
                customer_id_type2 += 1
            time.sleep(1)

    def start(self):
        self.__t.start()


class Customer:
    def __init__(self, customer_id):
        self.__t = Thread(target=self.__routine__)
        self.customer_id = customer_id
        self.beginServedEvt = Event()

    def start(self):
        self.__t.start()

    def __routine__(self):
        pass

    def type(self):
        pass

    def description(self):
        return "Kunde " + str(self.type()) + "-" + str(self.customer_id)


class CustomerType1(Customer):
    def __init__(self, customer_id):
        Customer.__init__(self, customer_id)

    def __routine__(self):
        time.sleep(10.4)
        stations[0].enqueue(self)
        self.beginServedEvt.wait()
        stations[0].endServeEvt.wait()
        time.sleep(5)
        stations[2].enqueue(self)
        self.beginServedEvt.wait()
        stations[2].endServeEvt.wait()
        print(self.description() + " ist fertig\n")

    def type(self):
        return 1


class CustomerType2(Customer):
    def __init__(self, customer_id):
        Customer.__init__(self, customer_id)

    def __routine__(self):
        time.sleep(30)
        stations[1].enqueue(self)
        self.beginServedEvt.wait()
        stations[1].endServeEvt.wait()
        print(self.description() + " ist fertig\n")

    def type(self):
        return 2


class Station:
    def __init__(self, description):
        self.description = description
        self.__current_customer__ = None
        self.__customer_queue__ = Queue()
        self.enqueue_Evt = Event()
        self.endServeEvt = Event()
        self.__t = Thread(target=self.__routine__)

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
        return len(self.__customer_queue__)

    def queue_is_empty(self):
        return self.__customer_queue__.empty()

    def __routine__(self):
        while True:
            self.enqueue_Evt.clear()
            while self.queue_is_empty():
                self.enqueue_Evt.wait()
            customer = self.dequeue()
            print(customer.description() + " wird bei " + self.description + " bedient\n")
            time.sleep(10)
            print(customer.description() + " verlässt " + self.description + "\n")
            self.endServeEvt.set()

    def start(self):
        self.__t.start()


stations = [Station("Bäcker"), Station("Wursttheke"), Station("Käsetheke"), Station("Kasse")]

if __name__ == '__main__':
    for s in stations:
        s.start()

    customerSpawner = CustomerSpawner()
    customerSpawner.start()
