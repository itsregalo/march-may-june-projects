# Client side: for client to connect to the new server
import socket, select, sys

ClientMultiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 5000

# connect to the server
try:
    ClientMultiSocket.connect((host, port))
except socket.error as msg:
    print("Connection failed. Error Code : " + str(msg[0]) + " Message " + msg[1])

res = ClientMultiSocket.recv(1024)
print("Received data from server: " + str(res))

# keep the client’s server running without being interpreted
while True:
    # wait for at least one of the sockets to be ready for processing
    # set timeout to 1 second
    ready_to_read, ready_to_write, in_error = select.select([ClientMultiSocket], [], [], 1)
    if ready_to_read:
        # data received from server, process it
        res = ClientMultiSocket.recv(1024)
        print("Received data from server: " + str(res))
        if not res:
            break
    else:
        # send user input to the server
        ClientMultiSocket.send(bytes(input(""), "utf-8"))
        # receive data from the server
        res = ClientMultiSocket.recv(1024)
        # print the received data
        print("Received data from server: " + str(res))
# close the connection
ClientMultiSocket.close()
