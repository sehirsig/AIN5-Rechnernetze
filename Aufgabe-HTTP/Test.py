import requests
from bs4 import BeautifulSoup
from bs2json import bs2json
import re

username = input()
password = input()

server = 'https://moodle.htwg-konstanz.de/moodle/'
res1 = requests.get(server)


def search_login_token():
    text = res1.text
    start_pos = re.search('"logintoken" value="', text).regs[0][1]
    LENGTH = 32
    return text[start_pos: start_pos + LENGTH]


search_login_token()

login = {'logintoken': search_login_token(), 'username': username, 'password': password}
res2 = requests.post(server, login)
res3 = requests.get(server + 'mod/chat/gui_basic/index.php?id=354')
res4 = requests.post(server + 'mod/chat/gui_basic/index.php?id=354', 'Hallo')

print()
