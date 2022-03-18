import heapq


class EventList:
    queue = []
    def init(self):
        heapq.heapify(self.queue)

    def pop(self):
        return heapq.heappop(self.queue)

    def push(self, a):
        heapq.heappush(self.queue, a)


a = EventList()
print(a.queue)
a.push(2)
print(a.queue)
print(a.pop())
print(a.queue)