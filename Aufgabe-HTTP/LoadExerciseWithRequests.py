import requests
import re

print("Nutzername eingeben:")
username = input()
print("Passwort eingeben:")
password = input()

server = 'https://moodle.htwg-konstanz.de/moodle/'
session = requests.session()
response1 = session.get(server)
site = response1.text
moodleSession = response1.cookies.get("MoodleSession")
session_cookie = {'MoodleSession': moodleSession}


def search_login_token():
    start_pos = re.search('"logintoken" value="', site).regs[0][1]
    LENGTH = 32
    return site[start_pos: start_pos + LENGTH]


login = "username=" + username + "&password=" + password + "&logintoken=" + search_login_token()
response2 = session.post(server, login, cookies=session_cookie, allow_redirects=False)

pdf_url = server + 'pluginfile.php/346660/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf'
response2 = session.get(pdf_url, cookies=session_cookie, allow_redirects=False)
file = response2.content

session.close()
