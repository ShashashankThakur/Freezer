#############################
#           SERVER          #
#############################

import csv
from datetime import datetime
from socket import *

USER_DATABASE = "server_database1.csv"
FILES_DATABASE = "server_database2.csv"


def time():
    # Return date and time in format
    current_time = datetime.now()
    formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S] [SERVER]")
    return formatted_time


def log_print(*args, **kwargs):
    # Print function to include timestamps for logs
    print(f"{time()} ", end='')
    print(*args, **kwargs)


def validate_user(username, password):
    with open(USER_DATABASE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False


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

        while True:
            message = connection_socket.recv(1024).decode().split("$$$$$")
            message_type = message[0]

            """ USER VALIDATION """

            if message_type == "VALIDATE":
                validation_request = message
                username = validation_request[1]
                password = validation_request[2]
                if validate_user(username, password):
                    connection_socket.sendall(f"GRANTED$$$$${username} is a valid user".encode())
                else:
                    connection_socket.sendall(f"DENIED$$$$${username} is not a valid user".encode())
                    continue

            """ FILE UPLOAD/DOWNLOAD """

            if message_type == "UPLOAD":
                file_transfer = message
                filename = file_transfer[1]
                log_print("Receiving file:", filename)
                with open(filename, 'wb') as f:
                    while True:
                        data = connection_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                log_print("File received successfully!")

            else:
                pass

        connection_socket.close()
        log_print("Connection socket closed")

        log_print("Waiting for connections...")


if __name__ == "__main__":
    main()
