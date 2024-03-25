#############################
#           SERVER          #
#############################

import csv
from datetime import datetime
from socket import *

USER_DATABASE = "_database_server_1.csv"
FILES_DATABASE = "_database_server_2.csv"


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


def receive_file(connection_socket, filename):
    connection_socket.sendall(f"READY_TO_RECEIVE".encode())
    log_print("Ready to receive file from client client")
    log_print("Receiving file:", filename)
    with open(filename, 'wb') as f:
        while True:
            data = connection_socket.recv(1024)
            if data == b'##########\xFF##########':
                break
            f.write(data)

    log_print("File received from client")

    file_transfer_acknowledge = connection_socket.recv(1024).decode().split("$$$$$")
    if file_transfer_acknowledge[0] == "CONFIRM_TRANSFER" and file_transfer_acknowledge[1] == filename:
        connection_socket.sendall(f"TRANSFER_COMPLETE".encode())
        return True

    return False


def send_file(connection_socket, filename):
    log_print("Client is ready to receive file")
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            connection_socket.sendall(data)
    connection_socket.sendall(b'##########\xFF##########')  # signal end of transmission

    log_print("File sent")
    connection_socket.sendall(f"CONFIRM_TRANSFER$$$$${filename}".encode())
    file_transfer_acknowledge = connection_socket.recv(1024).decode()
    if file_transfer_acknowledge == "TRANSFER_COMPLETE":
        log_print("File received by client successfully")
        return True

    else:
        log_print("No confirmation message received from client")
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

        user_validated = False

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
                    log_print(f"User {username} has logged on")
                    user_validated = True
                    continue
                else:
                    connection_socket.sendall(f"DENIED$$$$${username} is not a valid user".encode())
                    continue

            """ FILE UPLOAD """

            if message_type == "UPLOAD" and user_validated is True:
                file_transfer = message
                filename = file_transfer[1]

                receive_file(connection_socket, filename)

            """ FILE DOWNLOAD """

            if message_type == "DOWNLOAD" and user_validated is True:
                file_transfer = message
                filename = file_transfer[1]
                file_transfer_response = connection_socket.recv(1024).decode()

                if file_transfer_response == "READY_TO_RECEIVE":

                    send_file(connection_socket, filename)

            else:
                break

        connection_socket.close()
        log_print("Connection socket closed")

        log_print("Waiting for connections...")


if __name__ == "__main__":
    main()
