from time import sleep

import requests
import re

MESSAGE = 'HalloBotTest'

print("Nutzername eingeben:")
username = input()
print("Passwort eingeben:")
password = input()
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

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


# Aufgabe 1, in Moodle einloggen
token = search_login_token()
payload = {'anchor': '', 'logintoken': token, 'username': username, 'password': password}
response2 = session.post(server + "/login/index.php", data=payload, cookies=session_cookie, allow_redirects=False)

rechnernetze_seite = session.get("https://moodle.htwg-konstanz.de/moodle/course/view.php?id=5256")
if "Rechnernetze" in rechnernetze_seite.text:
    print("Anmeldung hat funktioniert!")
else:
    print("Anmelden hat NICHT funktioniert!")

# Aufgabe 2, Aufgabenstellung herunterladen
pdf_url = server + 'pluginfile.php/346660/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf'
response3 = session.get(pdf_url, cookies=session_cookie, allow_redirects=False)
# print("Response 3: " + response3.text)
file = response3.content

# Aufgabe 3, in Lab5Chat eine Nachricht abrufen und eine Nachricht senden
payload = {'id': '354'}
get_command = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=354"
response44 = session.get(get_command, data=payload, cookies=session_cookie)

# print("Read Labchat:\n " + response44.text)

#Get Chat SID Call
url = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_header_js/index.php?id=354"
url_response = session.get(url, cookies=session_cookie)


def getChatSid():
    start_pos = re.search('chat_sid=', url_response.text).regs[0][1]
    LENGTH = 32
    chat_sid = url_response.text[start_pos: start_pos + LENGTH]
    return chat_sid


chat_sid = getChatSid()

#Get Chat Messages

get_command = f"https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_header_js/jsupdate.php?chat_sid={chat_sid}&chat_lasttime=1655817052&chat_lastrow=0"
response_msg = session.get(get_command, cookies=session_cookie)
messages = response_msg.text.split("if(parent.msg)parent.msg.document.write")

for mesg in messages:
    if '<span class=\\"title\\">' in mesg:
        NACHRICHT = mesg.split('<span class=\\"title\\">')[1].split('<\/span>: <p>')
        print(NACHRICHT[0] + ": " + NACHRICHT[1].split('<\/p>')[0])




def getSesskey():
    start_pos = re.search('"sesskey":"', response44.text).regs[0][1]
    LENGTH = 10
    return response44.text[start_pos: start_pos + LENGTH]


def getLast():
    start_pos = re.search('name="last" value="', response44.text).regs[0][1]
    LENGTH = 10
    return response44.text[start_pos: start_pos + LENGTH]


print("Nachricht eingeben:")
MESSAGE = input()

post_command = 'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php'
sess_key = getSesskey()
last_key = getLast()
#print(f"SessKey: {sess_key}")
#print(f"Last: {last_key}")
payload = {'message': 'HalloBotTest', 'id': '354', 'groupid': '0', 'last': last_key, 'sesskey': sess_key}
payload = {'message': MESSAGE, 'id': '354', 'groupid': '0', 'last': last_key, 'sesskey': sess_key}
response_sendChat = session.post(post_command, data=payload, cookies=session_cookie, allow_redirects=False)
# print("Response SendChat: " + response_sendChat.text)
# print(response_sendChat.text)


# Aufgabe 4, Abgabe dieser Laborübung hochladen
# Benötigt: Post Command, MoodleSession Cookie.
post_command = 'https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php?id=219345&action=editsubmission'

response5 = session.get(post_command, cookies=session_cookie)

files = {'repo_upload_file': open('test2.pdf', 'rb'), 'sesskey': sess_key, 'repo_id': '3', 'itemid': '838689255',
         'author': 'Johannes Wirbser', 'savepath': '/', 'title': "Test", 'ctx_id': '346660'}
response5 = session.post(post_command, files=files, cookies=session_cookie, allow_redirects=False)
submission_site = response5.text

post_command = 'https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php'

# first post from upload
files = {'id': 219345, 'sesskey': sess_key, 'action': 'savesubmission', 'files_filemanager': '838689255',
         '_qf__mod_assign_submission_form': '1', 'userid': "19511"}
response5 = session.post(post_command, files=files, cookies=session_cookie, allow_redirects=False)


# print("Response 5: " + response5.text)

def get_client_id():
    start_pos = re.search('"client_id":"', submission_site).regs[0][1]
    LENGTH = 13
    return submission_site[start_pos: start_pos + LENGTH]


# second post from upload
client_id = get_client_id()
files = {'sesskey': sess_key, 'client_id': client_id, 'filepath': '/', 'item_id': '5369759423654'}
response5 = requests.post(post_command, files=files, cookies=session_cookie, allow_redirects=False)

# Gepostete Files speichern/abgeben
post_command = 'mod/assign/view.php HTTP/1.1'
payload = {'submitbutton': '%C3%84nderungen+speichern', }
session.post(server + post_command, data=payload, cookies=session_cookie, allow_redirects=False)
# print(response2.text)
session.close()
