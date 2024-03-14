#############################
#           SERVER          #
#############################

from datetime import datetime
from socket import *


def time():
    # Return date and time in format
    current_time = datetime.now()
    formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S] [SERVER]")
    return formatted_time


def log_print(*args, **kwargs):
    # Print function to include timestamps for logs
    print(f"{time()} ", end='')
    print(*args, **kwargs)


def main():
    hostport = 13000

    server_socket = socket(AF_INET, SOCK_STREAM)
    log_print("Welcoming socket created")
    server_socket.bind(("", hostport))
    server_socket.listen(1)
    log_print("Welcoming socket ready")
    log_print("Waiting for connections...")

    while True:
        connection_socket, client_address = server_socket.accept()
        log_print("Connection Socket created")
        log_print(f"Connected to {client_address[0]} port {client_address[1]}")
        log_print("Ready to receive...")

        filename = connection_socket.recv(1024).decode()
        log_print("Receiving file:", filename)
        with open(filename, 'wb') as f:
            while True:
                data = connection_socket.recv(1024)
                if not data:
                    break
                f.write(data)
        log_print("File received successfully!")

        connection_socket.close()
        log_print("Connection socket closed")

        log_print("Waiting for connections...")


if __name__ == "__main__":
    main()
