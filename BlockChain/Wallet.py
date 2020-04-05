import SocketUtils
import Transaction
import Signatures
import threading
import Miner
import time

headBlocks = [None]
wallets = [('localhost', 5006)]

#Add newBlock to the existing blockchain


def walletServer(myAddr):
    return True
    server = SocketUtils.newServerConnection('localhost', 5006)
    for i in range(30):
        newBlock = SocketUtils.recvObj(server)
        if newBlock:
            break
    server.close()

    for b in headBlocks:
        if newBlock.previousHash() == b.computeHash():
            newBlock.previousBlock = b
            headBlocks.remove(b)
            headBlocks.append(newBlock)

def getBalance(publKey):
    return 0.0

def sendCoins(publSend, amountSent, privSend, publRecv, amountRecv):
    return True


if __name__ == "__main__":
    minerPriv, minerPubl = Signatures.generate_keys()
    t1 = threading.Thread(target = Miner.minerServer, args = (('localhost',5005),))
    t2 = threading.Thread(target = Miner.nonceFinder, args = (wallets, myPubl,))
    t3 = threading.thread(target = walletServer, args = (('localhost', 5006),))
    t1.start()
    t2.start()
    t3.start()

    priv1, publ1 = Signatures.generate_keys()
    priv2, publ2 = Signatures.generate_keys()
    priv3, publ3 = Signatures.generate_keys()

    #Query Balance
    bal1 = getBalance(publ1)
    bal2 = getBalance(publ2)
    bal3 = getBalance(publ3)

    #Send Coins
    sendCoins(publ1, 1.0, priv1, publ2, 1.0)
    sendCoins(publ1, 1.0, priv1, publ3, 0.3)

    time.sleep(30)

    #Query Balances again
    new1 =  getBalance(publ1)
    new2 =  getBalance(publ2)
    new3 =  getBalance(publ3)

    #Verify Balances
    if (new1 - bal1 + 1.3) > 0.000001:
        print("Error, wrong balance for publ1")
    else:
        print("Success, good balance found for publ1")
    if (new2 - bal2 - 1) > 0.000001:
        print("Error, wrong balance for publ2")
    else:
        print("Success, good balance found for publ2")
    if (new3 - bal3 + 0.3) > 0.000001:
        print("Error, wrong balance for publ3")
    else:
        print("Success, good balance found for publ3")

    Miner.breakNow = True

    t1.join()
    t2.join()
    t3.join()

    print("Exit successful")

