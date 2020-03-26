import socket
import pickle
import select

TCP_PORT = 5005

def sendObj(ipAddr, inObj):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipAddr, TCP_PORT))
    data = pickle.dumps(inObj)
    s.send(data)
    s.close()
    return False

BUFFER_SIZE = 1024

def newServerConnection(ipAddr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ipAddr, TCP_PORT))
    s.listen()
    return s

def recvObj(socket):
    inputs, outputs, errors = select.select([socket], [], [socket], 6) #timeout 6 seconds
    if socket in inputs:
        newSocket, addr = socket.accept()
        allData = b''
        while True:
            data = newSocket.recv(BUFFER_SIZE)
            if not data:
               break
            allData = allData + data
        return pickle.loads(allData)
    return None
    

if __name__ == "__main__":
    server = newServerConnection('localhost')
    O = recvObj(server)
    #print("Success, returned without blocking")
    #print(O)
    server.close()