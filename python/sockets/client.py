import socket, select, string, sys

# set helper function
def display_menu():
    you = "You: "
    sys.stdout.write(you)
    sys.stdout.flush()

def main():
    if len(sys.argv)<2:
        host = input("Enter host: ")
    else:
        host = sys.argv[1]

    port = 5000

    # prompt for username
    username = input("Enter username: ")
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host. You can start sending messages')

    # send username to server if connected
    s.send(username.encode())
    # display menu
    display_menu()

    while 1:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
            else:
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg.encode())
                display_menu()

if __name__ == "__main__":
    main()
            