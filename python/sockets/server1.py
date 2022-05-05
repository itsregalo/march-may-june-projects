import socket, select, sys

from numpy import record

# Function to send message to all connected clients
def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                CONNECTION_LIST.remove(socket)

# Function to send message private to a client
def send_private_data (sock, message):
    for socket in PRIVATE_CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                PRIVATE_CONNECTION_LIST.remove(socket)

if __name__ == '__main__':
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    PRIVATE_CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
    HOST = '127.0.0.1'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    CONNECTION_LIST.append(server_socket)
    print("Chat server started on port " + str(PORT))

    while True:
        name = ''
        record = {}
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(sockfd, "Client (%s, %s) connected" % addr)
                # record the client name
                record[sockfd] = addr[0]
                # if user repeats the username
                if name in record.values():
                    # send a message to the client as bytes object
                    sockfd.send(b"Username already taken. Please choose another username.")
                    del record[sockfd]
                    CONNECTION_LIST.remove(sockfd)
                    sockfd.close()
                    continue
                else:
                    # add name and address
                    record[sockfd] = name
                    print("Client (%s, %s) connected" % addr," [",record[sockfd],"]")
                    sockfd.send(b"Welcome to the chat server")
            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # broadcast message
                        broadcast_data(sock, "\r" + '<' + str(record[sock]) + '> ' + data)
                        # send private message
                        if data.startswith('@'):
                            # get the name of the client
                            name = data.split('@')[1]
                            # get the message
                            message = data.split('@')[2]
                            # send private message
                            send_private_data(sock, "\r" + '<' + str(record[sock]) + '> ' + message)
                        # if the client sends the message "quit"
                        if data == "quit":
                            # remove the client from the list
                            CONNECTION_LIST.remove(sock)
                            PRIVATE_CONNECTION_LIST.remove(sock)
                            # send a message to the client
                            sock.send(b"Client disconnected")
                            # close the socket
                            sock.close()
                            # remove the client from the list
                            CONNECTION_LIST.remove(sock)
                            PRIVATE_CONNECTION_LIST.remove(sock)
                            # send a message to the client
                            broadcast_data(sock, "Client (%s, %s) disconnected" % addr)
                except:
                    # send a message to the client
                    sock.send(b"Client disconnected")
                    # close the socket
                    sock.close()
                    # remove the client from the list
                    CONNECTION_LIST.remove(sock)
                    PRIVATE_CONNECTION_LIST.remove(sock)
                    # send a message to the client
                    broadcast_data(sock, "Client (%s, %s) disconnected" % addr)
                    continue
    server_socket.close()