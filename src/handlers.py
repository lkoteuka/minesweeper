import datetime
from threading import Thread, Event


class MyThread(Thread):
    """
    Class for update timer in a separate thread.
    """
    def __init__(self, root, seconds_to_wait):
        """
        Constructor

        :param root: timer
        :type root: Timer
        :param seconds_to_wait: time between updates
        :type seconds_to_wait: int
        """
        Thread.__init__(self)
        self.daemon = True
        self.root = root
        self.stopped = Event()
        self.seconds_to_wait = seconds_to_wait

    def run(self):
        """
        Updating timer's clock. Override method of class Thread
        """
        while not self.stopped.wait(self.seconds_to_wait):
            self.root.update_clock()
        self.join()


class Timer:
    """
    Class for representing timer.
    """
    def __init__(self, text_variable):
        """
        Constructor

        :param text_variable: holder in GUI where time is shown
        :type text_variable: tk.StringVar
        """
        self.text_variable = text_variable
        self.is_stopped = False
        self.begin = datetime.datetime.now()
        self.reset_clock()
        self.update_clock()
        self.thread = MyThread(self, 1)
        self.thread.start()

    def update_clock(self):
        """
        Function for updating clock every tick
        """
        if self.is_stopped:
            return
        delta = datetime.datetime.now() - self.begin
        text = '{:0>2}:{:0>2}'.format(delta.seconds // 60, delta.seconds % 60)
        self.text_variable.set(text)

    def stop_clock(self):
        """
        Function for stopping clock
        """
        self.is_stopped = True

    def reset_clock(self):
        """
        Function for resetting clock
        """
        self.begin = datetime.datetime.now()
        self.is_stopped = False
        self.update_clock()
