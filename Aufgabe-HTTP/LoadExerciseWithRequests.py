from time import sleep

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
get_command = '/mod/chat/gui_basic/index.php?id=354 HTTP/1.1'
response44 = session.get(server + get_command, cookies=session_cookie)
#print("Response 44: " + response44.text)

post_command = '/mod/chat/gui_basic/index.php HTTP/1.1'
payload = {'message': 'HalloTest', 'id':  354, 'groupid': 0}
response_sendChat = session.post(server+get_command,data=payload, cookies=session_cookie)
#print("Response SendChat: " + response_sendChat.text)

post_command = '/mod/chat/gui_header_js/insert.php HTTP/1.1'
chat_sid = ""
payload = {'chat_sid': chat_sid, 'chat_message': "Hallo"}
response4 = session.post(server + post_command, data=payload, cookies=session_cookie)
#print("Response 4: " + response4.text)

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
