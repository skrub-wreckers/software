from sw.taskqueue import TaskQueue, TaskCancelled
import time

def print_ints():
    i = 0
    while True:
        print i
        i = i + 1
        time.sleep(0.25)
        try:
            yield
        except TaskCancelled:
            print('No more printing')
            raise


queue = TaskQueue()

t = queue.enqueue(print_ints)

time.sleep(1)

t.cancel()