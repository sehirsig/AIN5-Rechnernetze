import socket
import time
import threading



def connectThem(number):
    start = time.time();
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    # print('TCP Client created')
    Server_IP = '141.37.168.26'
    Server_PORT = number
    print(Server_PORT)
    #print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
    try:
        sock_return = sock.connect_ex((Server_IP, Server_PORT))
        if sock_return == 0:
            msg = "Hello"
            sock.send(msg)
            answer = sock.recv(1024)
            print("-->" + "Ergebnis Socket " + str(number) + ": " + str(answer) + " at " + str(time.time() - start) + "\n")
        else:
            print("Port " + str(number) + " has Error code " + str(sock_return) + " at " + str(time.time() - start) + "\n")
    except Exception as e:
        print("-->" + str(number) + " Failed." + " at " + str(time.time() - start) + " with error: " + str(e) + "\n")
        #print('Socket timed out at', time.asctime())
    sock.close()


for i in range(1,51):
    t1 = threading.Thread(target=connectThem, args=(i,))
    t1.start()
