from ThreadPool import task, pool
import time

class SimpleTask(task.Task):
    def __init__(self, callable):
        super(SimpleTask, self).__init__(callable)

def process():
    time.sleep(1)
    print('This is a SimpleTask 1')
    time.sleep(1)
    print('This is a SimpleTask 2')

def test():
    #initalize a thread pool
    test_pool = pool.ThreadPool()
    test_pool.start()

    #generate tasks
    for i in range(10):
        simple_task = SimpleTask(process)
        test_pool.put(simple_task)

def test_async_task():
    def async_process():
        num = 0
        for i in range(100):
            num += i
        return num
    # initalize a thread pool
    test_pool = pool.ThreadPool()
    test_pool.start()

    # generate tasks
    for i in range(10):
        async_task = task.AsyncTask(func=async_process)
        test_pool.put(async_task)
        result = async_task.get_result()
        print('Get result: %d' % result)

# test wait
def test_async_task2():

    def async_process():
        num = 0
        for i in range(100):
            num += i
        time.sleep(2)
        return num
    # initalize a thread pool
    test_pool = pool.ThreadPool()
    test_pool.start()

    # generate tasks
    for i in range(1):
        async_task = task.AsyncTask(func=async_process)
        test_pool.put(async_task)
        print('Get result in timestamp: %d' % time.time())
        result = async_task.get_result()
        print('Get result in timestamp: %d: %d' % (time.time(), result))


if __name__ == "__main__":
    # test()
    #test_async_task()
    test_async_task2()