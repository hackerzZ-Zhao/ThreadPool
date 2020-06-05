


import threading

class ThreadSafeQueueException():

    pass

class ThreadSafeQueue(object):
    pass

    def __init__(self, max_size = 0):
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.condition = threading.Condition()

    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    def put(self, item):
        if self.max_size != 0 and self.size() > self.max_size:
            return ThreadSafeQueueException

        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.put(item)

    def pop(self, block = False, timeout = 0):
        if self.size() == 0:
            if block:
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()
            else:
                return None

        self.lock.acquire()
        item = None
        if len(self.queue) > 0:
            item = self.queue.pop()
        self.lock.release()
        return item

    def get(self, index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item

