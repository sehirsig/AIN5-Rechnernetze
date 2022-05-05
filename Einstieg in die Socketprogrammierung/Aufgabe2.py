import base64
import socket

username = (base64.b64encode('rnetin'.encode('utf-8'))).decode('utf-8')
password = (base64.b64encode('Ueben8fuer8RN'.encode('utf-8'))).decode('utf-8')

mailserver_address = "asmtp.htwg-konstanz.de"
mailserver_port = 587

message = "Hello,\nThis is a test"
subject = "Test"
receiver = "johannes.wirbser@htwg-konstanz.de"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((mailserver_address, mailserver_port))

statement = "ehlo asmtp.htwg-konstanz.de\nAUTH LOGIN\n" + username + "\n" + password\
                    + "\nMAIL FROM: <rnetin@htwg-konstanz.de>\n"\
                    + "MAIL FROM: <renetest@htwg-konstanz.de>\n"\
                    + "rcpt to: <" + receiver + ">\n"\
                    + "data\nSubject: " + subject + "\n"\
                    + "\n" + message + "\n\n.\n"

s.send(statement.encode("utf8"))
s.close()
