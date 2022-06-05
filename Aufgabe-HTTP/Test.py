import base64
import socket

username = input()
password = input()

username = (base64.b64encode(username.encode('utf-8'))).decode('utf-8')
password = (base64.b64encode(password.encode('utf-8'))).decode('utf-8')

server = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_header_js/index.php?id=354"
port = 443

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((server, port))
