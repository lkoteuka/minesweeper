import datetime
from threading import Thread, Event


class MyThread(Thread):
    def __init__(self, root, seconds_to_wait):
        Thread.__init__(self)
        self.daemon = True
        self.root = root
        self.stopped = Event()
        self.seconds_to_wait = seconds_to_wait

    def run(self):
        while not self.stopped.wait(self.seconds_to_wait):
            self.root.update_clock()
        self.join()


class Timer():
    def __init__(self, text_variable):
        self.text_variable = text_variable
        self.reset_clock()
        self.update_clock()
        self.thread = MyThread(self, 1)
        self.thread.start()

    def update_clock(self):
        if self.is_stopped:
            return
        delta = datetime.datetime.now() - self.begin
        text = '{:0>2}:{:0>2}'.format(delta.seconds // 60, delta.seconds % 60)
        self.text_variable.set(text)

    def stop_clock(self):
        self.is_stopped = True

    def reset_clock(self):
        self.begin = datetime.datetime.now()
        self.is_stopped = False
        self.update_clock()
