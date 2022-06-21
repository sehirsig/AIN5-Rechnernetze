from time import sleep

import requests
import re

MESSAGE = 'HalloBotTest'

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

#Aufgabe 1, in Moodle einloggen
token = search_login_token()
payload = {'anchor': '', 'logintoken':  token, 'username': username, 'password': password}
response2 = session.post(server + "/login/index.php", data=payload, cookies=session_cookie, allow_redirects=False)

rechnernetze_seite = session.get("https://moodle.htwg-konstanz.de/moodle/course/view.php?id=5256")
if "Rechnernetze" in rechnernetze_seite.text:
    print("Anmeldung hat funktioniert!")
else:
    print("Anmelden hat NICHT funktioniert!")

#Aufgabe 2, Aufgabenstellung herunterladen
pdf_url = server + 'pluginfile.php/346660/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf'
response3 = session.get(pdf_url, cookies=session_cookie, allow_redirects=False)
#print("Response 3: " + response3.text)
file = response3.content

#Aufgabe 3, in Lab5Chat eine Nachricht abrufen und eine Nachricht senden
get_command = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=354"
response44 = session.get(get_command, cookies=session_cookie)
print("Read Labchat:\n " + response44.text)

def getSesskey():
    start_pos = re.search('"sesskey":"', response44.text).regs[0][1]
    LENGTH = 10
    return response44.text[start_pos: start_pos + LENGTH]

def getLast():
    start_pos = re.search('name="last" value="', response44.text).regs[0][1]
    LENGTH = 10
    return response44.text[start_pos: start_pos + LENGTH]

post_command = 'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php'
sess_key = getSesskey()
last_key = getLast()
print(sess_key)
print(last_key)
payload = {'message': MESSAGE,'id': '354', 'groupid': '0', 'last': last_key, 'sesskey': sess_key}
response_sendChat = session.post(post_command,data=payload, cookies=session_cookie)
#print("Response SendChat: " + response_sendChat.text)


#Aufgabe 4, Abgabe dieser Laborübung hochladen
# Benötigt: Post Command, MoodleSession Cookie.
post_command = '/repository/repository_ajax.php?action=upload HTTP/1.1'
files = {'upload_file': open('test2.pdf','rb')}

response5 = requests.post(server + post_command, files=files)
#print("Response 5: " + response5.text)

#Gepostete Files speichern/abgeben
post_command = '/mod/assign/view.php HTTP/1.1'
payload = {'submitbutton': '%C3%84nderungen+speichern',}
session.post(server + post_command, data=payload, cookies=session_cookie)
#print(response2.text)
session.close()
