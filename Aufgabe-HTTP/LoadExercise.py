import requests
import re
import http.client as client
from urllib.parse import urlparse


print("Nutzername eingeben:")
username = input()
print("Passwort eingeben:")
password = input()

server = 'moodle.htwg-konstanz.de'
con = client.HTTPSConnection(server)
con.request('GET', '/moodle/')
response = con.getresponse()
site = response.read().decode()


def search_login_token():
    start_pos = re.search('"logintoken" value="', site).regs[0][1]
    LENGTH = 32
    return site[start_pos: start_pos + LENGTH]


login = "username=" + username + "&password=" + password + "&logintoken=" + search_login_token()
con.request("POST", "/", body=login.encode("utf8"))
response = con.getresponse()
response.read()
con.request('GET', '/moodle/')
con.getresponse().read()
pdf_url = '/moodle/pluginfile.php/346660/mod_assign/introattachment/0/AIN RN - Laboraufgabe - HTTP.pdf?forcedownload=1'
pdf_url_parsed = urlparse(pdf_url).path.replace(" ", "")


con.request('GET', server + pdf_url_parsed)
response = con.getresponse()
file = response.read()
