import dis
import socket, select, sys

"""
To start chatting, client should get connected to
the server where it can experience two types of chatting, public where messages are
broadcasted to all connected users (clients) and private chatting where chatting only
occurs between two parties.
"""

# helper func
def display():
    sys.stdout.write('> ')
    sys.stdout.flush()


def main():
    if len(sys.argv) < 3:
        host = 'localhost'
        port = 5000
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    # ask for username, password and type of chat
    username = input('Enter username: ')
    password = input('Enter password: ')
    chat_type = input('Enter chat type: ')
    if chat_type == 'public':
        chat_type = 0
    elif chat_type == 'private':
        chat_type = 1
    else:
        print('Invalid chat type')
        return
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to the server
    try:
        s.connect((host, port))
    except socket.error as msg:
        print('Failed to connect. Error: ' + str(msg))
        sys.exit()
    # send username and password to the server
    s.send(username.encode('utf-8'))
    s.send(password.encode('utf-8'))
    s.send(str(chat_type).encode('utf-8'))

    display()
    while 1:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == s:
                # incoming message from server
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    print(data.decode('utf-8'))
                    display()
            else:
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg.encode('utf-8'))
                display()
                sys.stdin.flush()

if __main__ == "__main__":
    main()

