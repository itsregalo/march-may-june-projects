import socket, select, sys

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
    name=""

    # dictionary to store the username, password and type of chat
    user_details = {}
    
    # list to store the socket connections
    CONNECTION_LIST = []
    PRIVATE_CONNECTION_LIST = []

    buffer = 4096
    port = 8002
    # create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a port
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(10)

    # add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    print('Chat server started on port ' + str(port))

    # loop for ever
    while 1:
        # get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            # new connection
            if sock == server_socket:
                # accept the connection
                sockfd, addr = server_socket.accept()
                name = sockfd.recv(buffer).decode('utf-8')
                CONNECTION_LIST.append(sockfd)
                user_details[addr] = None

                # if user is already in the list, send a message to the user
                if name in user_details.values():
                    sockfd.send("Username already taken. Please try again".encode('utf-8'))
                    del user_details[addr]
                    CONNECTION_LIST.remove(sockfd)
                    sockfd.close()
                    continue
                else:
                    user_details[addr] = name
                    print('Got connection from', addr)
                    sockfd.send("Welcome to the chat server".encode('utf-8'))
                    broadcast_data(sockfd, '\r' + name + ' entered the chat\n')
                    # continue
           
            else:
                 # message from a client
                try:
                    newData = sock.recv(buffer)
                    data = newData[:newData.index(b'\n')]

                    # get address of the client
                    i, p = sock.getpeername()
                    # get the username of the client
                    
                    if data == 'BYE':
                        broadcast_data(sock, '\r' + user_details[(i, p)] + ' left the chat\n')
                        # user left the chat
                        print(user_details[(i, p)] + ' left the chat')
                        del user_details[(i, p)]
                        CONNECTION_LIST.remove(sock)
                        sock.close()
                        continue
                    else:
                        # send message to all connected clients
                        broadcast_data(sock, '\r' + user_details[(i, p)] + ': ' + data.decode('utf-8') + '\n')
                        # send message to all private clients
                        if data[0] == '@':
                            send_private_data(sock, '\r' + user_details[(i, p)] + ': ' + data.decode('utf-8') + '\n')
                        # continue
                except:
                    (i,p) = sock.getpeername()
                    broadcast_data(sock, '\r' + user_details[(i, p)] + ' left the chat\n')
                    # user left the chat
                    print(user_details[(i, p)] + ' left the chat')
                    del user_details[(i, p)]
                    CONNECTION_LIST.remove(sock)
                    sock.close()
                    continue
    server_socket.close()




                