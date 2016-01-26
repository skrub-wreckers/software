import threading
import sys
import inspect
import functools

class sleep(object):
    """A simple data object that should be yielded by a task to sleep interruptibly """
    def __init__(self, dur):
        self.dur = dur

class TaskQueue(object):
    def __init__(self):
        # contains the current task. Setting this is locked through _task_lock.
        self._task = None
        self._task_lock = threading.Condition()

        self._thread = threading.Thread(target=self._background)
        self._thread.daemon = True
        self._thread.start()

    def _background(self):
        with self._task_lock:
            while True:
                # get the next operation when notified by the main thread
                while self._task is None:
                    self._task_lock.wait()

                # run the task
                self._task._run()
                self._task = None

    def enqueue(self, task):
        """
        Enqueue a function to run, and block until it starts. Returns a Task
        object
        """
        task = Task(task)

        # wait until the background thread is ready
        with self._task_lock:
            self._task_lock.notify()
            self._task = task

        return task

def async_method_decorator(get_queue):
    """
    Create a decorator for use at class scope, given a function that obtains
    the queue from self.

        class Test(object):
            def __init__(self):
                self.queue = TaskQueue()

            _async = async_method_decorator(lambda self: self.queue)

            @_async
            def task(self, args):
                pass

        t = Test()
        t.task()
        t.task(async=True)
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(self, *args, **kwargs):
            t = get_queue(self).enqueue(lambda: f(self, *args, **kwargs))
            if kwargs.pop('async', False):
                return t
            else:
                return t.wait()

        return wrapped
    return decorator



class TaskCancelled(Exception):
    """Thrown at any `yield` in a task, if a cancel is requested"""
    pass

class Task(object):
    _exc_info = None
    _cancelled = False

    def __init__(self, f):
        self.f = f
        self._done = threading.Event()
        self._cancel_pending = threading.Event()

    def wait(self, *args, **kwargs):
        """
        Wait for the task to complete. Takes an optional timeout argument, and
        returns true if the task completed.

        If the task threw an exception on exit, rethrow it
        """
        res = self._done.wait(*args, **kwargs)

        if res and self._exc_info is not None:
            raise self._exc_info[0], None, self._exc_info[2]

        return res

    def cancel(self):
        """
        Request a cancel of the task

        Return true if the cancel was acknowledged, and false if the task was
        about to exit anyway.
        """
        self._cancel_pending.set()
        self.wait()
        return self._cancelled

    def _run(self):
        """
        Private function called by the TaskQueue
        """
        try:
            # call the function
            gen = self.f()

            # if it contained yields
            if inspect.isgenerator(gen):
                while True:
                    try:
                        # cancel the task if appropriate
                        if self._cancel_pending.is_set():
                            val = gen.throw(TaskCancelled())

                        # otherwise continue on from the yield
                        else:
                            val = gen.next()

                        # if a sleep was requested, instead wait on the cancellation
                        if type(val) == sleep:
                            self._cancel_pending.wait(timeout=val.dur)

                    except StopIteration:
                        # task exited normally (possibly ignoring the cancel)
                        break

        except TaskCancelled:
            self._cancelled = True
        except Exception:
            print('There was an exception in a queued task')
            self._exc_info = sys.exc_info()
            import traceback
            traceback.print_exception(*self._exc_info)
            print()
        
        self._done.set()
