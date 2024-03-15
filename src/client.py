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


def main():

    hostname = "localhost"
    hostport = 13000

    client_socket = socket(AF_INET, SOCK_STREAM)
    log_print("Socket created")

    client_socket.connect((hostname, hostport))
    log_print("Connected to server")

    """ USER VALIDATION """

    while True:
        username = input("Username: ")
        password = input("Password: ")  # hide characters on screen

        validation_request = f"VALIDATE$$$$${username}$$$$${password}"
        client_socket.sendall(validation_request.encode())  # encrypt validation message

        validation_response = client_socket.recv(1024).decode()
        if validation_response.startswith("GRANTED"):
            break
        else:
            log_print("Invalid username or password")

    """ FILE UPLOAD/DOWNLOAD """

    filename = input("Filename: ")

    client_socket.sendall(f"UPLOAD$$$$${filename}".encode())

    with open(filename, 'rb') as f:
        while True:
            # chunks of 1024 bits
            data = f.read(1024)
            if not data:
                break
            client_socket.sendall(data)

    log_print("File sent successfully!")

    client_socket.close()
    log_print("Socket closed")


if __name__ == "__main__":
    main()
