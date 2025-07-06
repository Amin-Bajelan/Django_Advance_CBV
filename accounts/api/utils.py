import threading


class EmailThreading(threading.Thread):

    def __init__(self, email_obg):
        threading.Thread.__init__(self)
        self.email_obg = email_obg

    def run(self):
        self.email_obg.send()
