import socket

ipAddr =  '192.168.0.39'    
port = 5005
bufferSize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#have client connect to server we created
s.connect(ipAddr, port)

s.send("Hello World")
data = s.recv(bufferSize)
print("Recieved: " + data)

s.close()

