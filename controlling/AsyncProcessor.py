class AsyncProcessor(object):
    def __init__(self, thread_pool):
        self._thread_pool = thread_pool

    def enqueue(self, action):
        self._thread_pool.submit(self._execute_and_log_if_exception, action)

    def _execute_and_log_if_exception(self, action):
        try:
            action()
        except Exception as e:
            print("*** EXCEPTION IN THREAD ***")
            print(str(e))
