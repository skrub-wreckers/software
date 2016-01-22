import threading

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
                op()

                # notify the main thread that we finished the command
                with self._op_done:
                    self._op_done.notify_all()
                    self._op = None

    def enqueue(self, task):
        # wait until the background thread is ready
        with self._busy_lock:
            self._busy_lock.notify()
            self._op = task

        # wait until the background thread is done
        with self._op_done:
            self._op_done.wait()
