import socket
import pickle
import select

TCP_PORT = 5005
BUFFER_SIZE = 1024 

def newServerConnection(ipAddr, port = TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ipAddr, port))
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

def sendObj(ipAddr, inObj, port = TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipAddr, port))
    data = pickle.dumps(inObj)
    s.send(data)
    s.close()
    return False

    

if __name__ == "__main__":
    server = newServerConnection('localhost')
    O = recvObj(server)
    #print("Success, returned without blocking")
    #print(O)
    server.close()