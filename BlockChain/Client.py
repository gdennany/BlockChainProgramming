import TxBlock
import Transaction
import Signatures
import pickle
import socket

TCP_PORT = 5005

def sendBlock(ipAddr, block):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipAddr, TCP_PORT))
    data = pickle.dumps(block)
    s.send(data)
    s.close()
    return False

if __name__ == "__main__":
    priv1, publ1 = Signatures.generate_keys()
    priv2, publ2 = Signatures.generate_keys()
    priv3, publ3 = Signatures.generate_keys()
    
    Tx1 = Transaction.Tx()
    Tx1.add_input(publ1, 2.3)
    Tx1.add_output(publ2, 1.0)
    Tx1.add_output(publ3, 1.1)
    Tx1.sign(priv1)

    Tx2 = Transaction.Tx()
    Tx2.add_input(publ3, 2.3)
    Tx2.add_input(publ2, 1.0)
    Tx2.add_output(publ1, 3.1)
    Tx2.sign(priv2)
    Tx2.sign(priv3)

    Block1 = TxBlock.TxBlock(None)
    Block1.addTx(Tx1)
    Block1.addTx(Tx2)

    sendBlock('192.168.2.12', Block1)
    sendBlock('192.168.2.12', Tx2)





