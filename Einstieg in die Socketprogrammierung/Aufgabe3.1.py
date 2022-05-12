import base64
from socket import *

#Variablen
MSG = """Subject: Python Email
Das hier ist eine Python Email
Automatisch verschickt!

\r\n.\r\n
"""

MSG_SIZE = 1024

MAILSERVER = "asmtp.htwg-konstanz.de"
ASMPT_PORT = 587

SENDER_USERNAME = 'rnetin'
SENDER_PASSWORD = 'Ueben8fuer8RN'

SENDER_EMAIL = '<spoofedTest@test.com>'
RCPT = '<sebastian.hirsig@htwg-konstanz.de>'

username = (base64.b64encode(SENDER_USERNAME.encode('utf-8'))).decode('utf-8')
password = (base64.b64encode(SENDER_PASSWORD.encode('utf-8'))).decode('utf-8')


print(username)
print(password)

#Create Sockets
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((MAILSERVER, ASMPT_PORT))

recv = clientSocket.recv(MSG_SIZE).decode()

print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

#EHLO Command
ehlo_command = 'ehlo ' + MAILSERVER + '\r\n'
clientSocket.send(ehlo_command.encode())

recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#Login
authlogin_command = 'AUTH LOGIN\r\n'
clientSocket.send(authlogin_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

username_command = username + '\r\n'
clientSocket.send(username_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

password_command = password + '\r\n'
clientSocket.send(password_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#MAIL FROM
msgfrom_command = 'MAIL FROM: ' + SENDER_EMAIL + '\r\n'
clientSocket.send(msgfrom_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#RCPT TO
rcptto_command = 'RCPT TO: ' + RCPT + '\r\n'
clientSocket.send(rcptto_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#DATA
data_command = 'DATA\r\n'
clientSocket.send(data_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#MESSAGE
msg_command = MSG
clientSocket.send(msg_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#LOGOUT
logout_command = 'QUIT\r\n'
clientSocket.send(logout_command.encode())
recv = clientSocket.recv(MSG_SIZE).decode()
print(recv)

#Kommandozeileneingabe
#Dism /Online /Enable-Feature /FeatureName:TelnetClient
#telnet asmtp.htwg-konstanz.de 587
#ehlo asmtp.htwg-konstanz.de
#AUTH LOGIN
#cm5ldGlu
#VWViZW44ZnVlcjhSTg==
#MAIL FROM: <rnetin@htwg-konstanz.de>
#MAIL FROM: <renetest@htwg-konstanz.de>
#rcpt to: <sebastian.hirsig@htwg-konstanz.de>
#data
#Subject: Test
#
#Hello,
#This is a test
#
#.

