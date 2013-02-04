import time
from threading import Thread
from spynach.thread_locals import ThreadLocalProxy

request = ThreadLocalProxy()

class TestThreadLocals:
    def test_concurrecy(self):
        values = []
        def value_setter(idx):
            time.sleep(0.01 * idx)
            request._set_object(idx)
            time.sleep(0.02)
            values.append(request._get_object())
            request._pop_object()

        expected_value = range(1, 40)
        threads = [Thread(target=value_setter, args=(x,)) for x in expected_value]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        assert sorted(values) == expected_value
