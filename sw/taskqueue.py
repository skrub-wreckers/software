import threading
import sys
import inspect

class TaskQueue(object):
    def __init__(self):
        # contains the current operation. Setting this is locked through
        # _busy_lock. Upon completion, this is cleared locked on op_done.
        self._op = None
        self._busy_lock = threading.Condition()
        self._op_done = threading.Condition()

        self._thread = threading.Thread(target=self._background)
        self._thread.daemon = True
        self._thread.start()

    def _background(self):
        """ run in the background """
        while True:
            # lock on _busy_lock to prevent the main thread from changing the
            # command without it being looked at
            with self._busy_lock:
                # get the next operation when notified by the main thread
                while self._op is None:
                    self._busy_lock.wait()
                op = self._op

                # delegate to the appropriate control method
                op._run()

                # notify the main thread that we finished the command
                with self._op_done:
                    self._op_done.notify_all()
                    self._op = None

    def enqueue(self, task):
        task = Task(task)

        # wait until the background thread is ready
        with self._busy_lock:
            self._busy_lock.notify()
            self._op = task

        return task

class TaskCancelled(Exception):
    pass

class Task(object):
    _exc_info = None
    _cancelled = False

    def __init__(self, f):
        self.f = f
        self._done = threading.Event()
        self._cancel_pending = threading.Event()

    def wait(self, *args, **kwargs):
        res = self._done.wait(*args, **kwargs)

        if res and self._exc_info is not None:
            raise self._exc_info[0], None, self._exc_info[2]

        return res

    def cancel(self):
        self._cancel_pending.set()
        self.wait()

    def _run(self):
        try:
            # call the function
            gen = self.f()

            # if it contained yields
            if inspect.isgenerator(gen):
                while True:
                    try:
                        # cancel the task if appropriate
                        if self._cancel_pending.is_set():
                            gen.throw(TaskCancelled())

                        # otherwise continue on from the yield
                        else:
                            gen.next()

                    except StopIteration:
                        # task exited normally (possibly ignoring the cancel)
                        break

        except TaskCancelled:
            self._cancelled = True
        except Exception:
            self._exc_info = sys.exc_info()

        self._done.set()
