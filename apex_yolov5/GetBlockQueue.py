import queue
import threading


class GetBlockQueue:
    def __init__(self, name, maxsize=1):
        self.name = name
        self.lock = threading.Lock()
        self.queue = queue.Queue(maxsize=maxsize)

    def get(self):
        o = self.queue.get()
        return o

    def put(self, data):
        with self.lock:
            while True:
                try:
                    self.queue.put(data, block=False)
                    break
                except queue.Full:
                    try:
                        self.queue.get_nowait()
                    except queue.Empty:
                        pass
        # print("[{}]put操作后队列大小：{}".format(self.name, self.queue.qsize()))

    def clear(self):
        with self.lock:
            while not self.queue.empty():
                self.queue.get()
            # print("[{}]清空队列".format(self.name))
