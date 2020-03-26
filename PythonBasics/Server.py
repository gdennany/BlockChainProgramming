#implementation of an echo server

import socket
import select

ipAddr =  '192.168.0.39'    # local IP address
port = 5005                 # could be anything, declare any port number youd like

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ipAddr, port))

#wait for client to connect
s.listen()

#accept 10 connections
for q in range(10):
    rd, wt, err = select.select([s],[],[s],6) #6 sec timeout 
    if s in rd:
        connection, addr = s.accept()

        while True:
            data = connection.recv()
            #if client has finished sending data (here an empty string) then exit and close socket
            if not data:
                break
            print("Recieved: " + data)
            #echo the data back to the client
            connection.send(data)
#close the socket connection
s.close()
    
