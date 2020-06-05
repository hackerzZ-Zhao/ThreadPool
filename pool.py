
import threading
import psutil

from ThreadPool.task import Task, AsyncTask
from ThreadPool.queue import ThreadSafeQueue


class ProcessThread(threading.Thread):

    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.dismiss_flag = threading.Event() #thread stop signal
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while True:
            if self.dismiss_flag.is_set():
                break

            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue
            result = task.callable(*task.args, **task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)


    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()

class ThreadPool:

    def __init__(self, size = 0):
        if not size:
            size = psutil.cpu_count() * 2 #the size of pool should be twice as CPU processor

        self.pool = ThreadSafeQueue(size)
        self.task_queue = ThreadSafeQueue()

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    #stop thread pool
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()


    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()

        self.task_queue.put(item)

    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.put(item)

    def size(self):
        return self.pool.size()

class TaskTypeErrorException(Exception):
    pass