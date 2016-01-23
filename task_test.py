from sw.taskqueue import TaskQueue, TaskCancelled
import time

def print_ints():
    try:
        i = 0
        while True:
            print i
            i = i + 1
            time.sleep(0.25)
            yield
    except TaskCancelled:
        print('No more printing')
        raise

def print_once():
    print "once"


def throw_once():
    raise "once"

queue = TaskQueue()

t = queue.enqueue(print_once)
t.wait()

t = queue.enqueue(throw_once)
try:
    t.wait()
except Exception as e:
    print(type(e))

t = queue.enqueue(print_ints)
time.sleep(1)
t.cancel()