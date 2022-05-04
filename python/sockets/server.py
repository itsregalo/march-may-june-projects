"""
configure a client server socket
programming based application. Multiple clients will be able to connect to a
server. Server should be able to perform statistics about the input data stream
provided by the clients and sending back the results to the clients
"""
import socket, select

# send message to all clients who are connected
def broadcast_data(sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == '__main__':
    name = ""

    # record all the clients who are connected
    record = {}
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(10) # max number of connections

    # add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))
    
    """
    Multiple clients will be able to connect to a
    server. Server should be able to perform statistics about the input data stream
    provided by the clients and sending back the results to the clients
    """
    while True:
        # get the list of sockets which are ready to be read
        # 4th arg, time out = 0, means it is non-blocking
        ready_to_read, ready_to_write, in_error = select.select(CONNECTION_LIST, [], [], 0)
        for sock in ready_to_read:
            # a new connection request received
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(sockfd, "Client (%s, %s) connected" % addr)
                # record the client name
                record[sockfd] = addr[0]

                # if user repeats the username
                if name in record.values():
                    sockfd.send("Username already taken!\n")
                    del record[sockfd]
                    CONNECTION_LIST.remove(sockfd)
                    sockfd.close()
                    continue
                else:
                    # add name and address
                    record[sockfd] = name
                    print("Client (%s, %s) connected" % addr," [",record[sockfd],"]")
                    sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m")
                    broadcast_data(sockfd, "\33[32m\r "+name+" joined the conversation \n\33[0m")

            # a message from a client
            else:
                # process data received from client
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # send data to all clients
                        broadcast_data(sock, data)
                    else:
                        # remove the socket that's broken
                        if sock in CONNECTION_LIST:
                            CONNECTION_LIST.remove(sock)
                        # at this stage, no data means probably the connection has been broken
                        broadcast_data(sock, "Client (%s, %s) is offline" % record[sock])
                        # remove client from record
                        del record[sock]
                        # close the socket
                        sock.close()
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % record[sock])
                    print("Client (%s, %s) is offline" % record[sock])
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()