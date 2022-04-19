import base64

username = (base64.b64encode('rnetin'.encode('utf-8'))).decode('utf-8')
password = (base64.b64encode('ntsmobil'.encode('utf-8'))).decode('utf-8')

mailserver_address = "asmtp.htwg-konstanz.de"
mailserver_port = 587

print(username)
print(password)

#Kommandozeileneingabe
#Dism /Online /Enable-Feature /FeatureName:TelnetClient
#telnet asmtp.htwg-konstanz.de 587
#ehlo asmtp.htwg-konstanz.de
#AUTH LOGIN
#cm5ldGlu
#bnRzbW9iaWw=
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

