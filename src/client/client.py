#############################
#           CLIENT          #
#############################

from datetime import datetime
from socket import *


def time():
    # Return date and time in format
    current_time = datetime.now()
    formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S] [CLIENT]")
    return formatted_time


def log_print(*args, **kwargs):
    # Print function to include timestamps for logs
    print(f"{time()} ", end='')
    print(*args, **kwargs)


def send_file(client_socket):

    """ FILE UPLOAD """

    filename = input("Filename: ")

    client_socket.sendall(f"UPLOAD$$$$${filename}".encode())

    file_transfer_response = client_socket.recv(1024).decode()

    if file_transfer_response == "READY_TO_RECEIVE":
        log_print("Server is ready to receive file")
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        log_print("File sent")

    # TODO: Error handling: File not found on client side

    client_socket.sendall(b'##########\xFF##########')  # signal end of transmission
    client_socket.sendall(f"CONFIRM_TRANSFER$$$$${filename}".encode())
    file_transfer_acknowledge = client_socket.recv(1024).decode()
    if file_transfer_acknowledge == "TRANSFER_COMPLETE":
        log_print("File received by server successfully")
        return True
    else:
        log_print("No confirmation message received from server")
        return False


def retrieve_file(client_socket):

    """ FILE DOWNLOAD"""

    filename = input("Filename: ")

    client_socket.sendall(f"DOWNLOAD$$$$${filename}".encode())
    client_socket.sendall("READY_TO_RECEIVE".encode())

    log_print("Receiving file:", filename)
    with open(filename, 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if data == b'##########\xFF##########':
                break
            f.write(data)

    log_print("File received from server")

    file_transfer_acknowledge = client_socket.recv(1024).decode().split("$$$$$")
    if file_transfer_acknowledge[0] == "CONFIRM_TRANSFER" and file_transfer_acknowledge[1] == filename:
        client_socket.sendall(f"TRANSFER_COMPLETE".encode())
        return True

    return False


def validate_user(client_socket):

    """ USER VALIDATION """

    while True:
        username = input("Username: ")
        password = input("Password: ")  # hide characters on screen

        validation_request = f"VALIDATE$$$$${username}$$$$${password}"
        client_socket.sendall(validation_request.encode())  # encrypt validation message

        validation_response = client_socket.recv(1024).decode()
        if validation_response.startswith("GRANTED"):
            return True
        else:
            log_print("Invalid username or password")
            return False


def main():
    hostname = "localhost"
    hostport = 13000

    client_socket = socket(AF_INET, SOCK_STREAM)
    log_print("Socket created")

    client_socket.connect((hostname, hostport))
    log_print("Connected to server")

    if validate_user(client_socket):

        menu_option = input("Transmission (t) of Retrieval (r): ")

        if menu_option == "t":

            send_file(client_socket)

        elif menu_option == "r":

            retrieve_file(client_socket)

    client_socket.close()
    log_print("Socket closed")


if __name__ == "__main__":
    main()
