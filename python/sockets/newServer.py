import socket, os
from _thread import *

ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 5000

ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as msg:
    print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])

print("Server is running on port " + str(port))

# start listening to the clients
ServerSideSocket.listen(10)

# a list of clients
clients = []
