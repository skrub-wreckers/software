from sw.taskqueue import TaskQueue, TaskCancelled, sleep
import time

def print_ints():
    try:
        i = 0
        while True:
            print i
            i = i + 1
            yield sleep(0.25)
    except TaskCancelled:
        print('No more printing')
        raise

def print_once():
    print "once"


def throw_once():
    raise "once"

def long_wait():
    print "Begin"
    try:
        yield sleep(10)
    finally:
        print "aborted"

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

t = queue.enqueue(long_wait)
time.sleep(1)
t.cancel()