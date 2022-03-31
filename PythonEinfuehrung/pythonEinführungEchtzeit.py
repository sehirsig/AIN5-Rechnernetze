import time
from threading import Thread


def spawnCustomers():
    while (True):
        time.sleep(1)
        CustomerType1().start()
        time.sleep(1)
        CustomerType2().start()


class Customer:
    def __init__(self):
        self.__t = Thread(target=self.__routine__)

    def start(self):
        self.__t.start()

    def __routine__(self):
        pass


class CustomerType1(Customer):
    def __init__(self):
        Customer.__init__(self)

    def __routine__(self):
        print("Customer Type 1")


class CustomerType2(Customer):
    def __init__(self):
        Customer.__init__(self)

    def __routine__(self):
        print("Customer Type 2")


if __name__ == '__main__':
    customerSpawner = Thread(target=spawnCustomers)
    customerSpawner.start()
