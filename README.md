# Freezer

Freezer is a unique cloud storage client-server application. 
This project is my solo submission to a semester final group project, 
under professor Dr. Keyur Parmar, CS206 Computer Networks and Internet, 
NIT Surat.

## Introduction

A service provided by a popular chat application is exploited 
to provide the client with an "infinite and free" cloud storage. 
A file is sent to the server from the client. 
The server segments the raw file into small chunks of data. Each data 
segment is encrypted and stored on a chat. To retrieve the files, 
the client sends a request to the server, which decrypts and reassembles 
the file, and transmits it back to the client.

## Disclaimer

This project is created for educational and research purposes
 only. Using this application to exploit services provided by chat applications, 
bypass cloud storage services, or engage in illegal activities is strictly prohibited.
The developer of this project is not responsible for any misuse of this application.

## Documentation

The protocol built on top of TCP:
1. Validate user:
    - client send username and password to server
    - server validates username and password and sends result to client
    - client side databases:
        f(x): filenames -> client randomly generated names, keys
    - server side databases:
        f(x): usernames -> passwords
        g(x): client randomly generated name -> server randomly generated names, numbers of segments

2. Uploading a file:
    - user enters filename
    - client adds filename and a client randomly generated name and a key into the client database
    - client sends "sending file" market to the server
    - server is ready to accept file
    - client sends client randomly generated name
    - client encrypts the file with AES and key to create an encrypted file
    - client sends file in 100MB parts with part number
    - server accepts client randomly generated name
    - server adds client randomly generated name and a server randomly generated name and number of parts into the database
    - server accepts the file parts and names it the server randomly generated name with part number
    - server uploads the files into the discord server
3. Downloading a file:
    - user enters the file name
    - client searches for filename in database and gets corresponding client randomly generated name and key
    - client sends "requesting file" marker to server
    - client sends the client randomly generated name to the server
    - server receives the client randomly generated name
    - server searches for client randomly generated name in database and gets corresponding server randomly generated name and number of parts
    - server downloads the parts from the discord server
    - server sends the parts to the client
    - client assembles the parts and names it the filename
    - client decrypts the AES encrypted file with key to retrieve the original file