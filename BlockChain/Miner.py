import SocketUtils
import Transaction
import TxBlock
import Signatures
import threading
import time

wallets = [('localhost', 5005)]
txList = []
headBlocks = [None]
breakNow = False

def findLongestBlockChain():
    longest = -1
    longHead = None
    for b in headBlocks:
        current = b
        thisLen = 0
        while current != None:
            thisLen = thisLen + 1
            current = current.previousBlock()
        if thisLen > longest:
            longHead = b
            longest = thisLen
    return longHead

def minerServer(myAddr):
    global txList
    global breakNow
    myIp, myPort = myAddr
    #Open Server Connection
    server = SocketUtils.newServerConnection(myIp, myPort)
    #recieve transactions from wallets
    #for i in range(10):
    while not breakNow:
        print("Finding Nonce...")
        newTx = SocketUtils.recvObj(server)
        if isinstance(newTx, Transaction.Tx):
            txList.append(newTx)
            print("Recieved Tx")
        #if len(txList) >= 2:
        #    break
    
    
    return False

def nonceFinder(walletList, minerPubl):
    global breakNow
    
    #collect those transactions into a block
    while not breakNow:
        newBlock = TxBlock.TxBlock(findLongestBlockChain())
        for tx in txList:
            newBlock.addTx(tx)
    
        #compute and add mining reward
        totalIn, totalOut = newBlock.count_totals()
        mineReward = Transaction.Tx()
        mineReward.add_output(minerPubl, 25.0 + totalIn - totalOut)
        newBlock.addTx(mineReward)
        
        #Mine (i.e. find a satisfying nonce)
        newBlock.find_nonce(10000)
        if newBlock.good_nonce():
            print("Good nonce found")
        
        #send that new block to each in walletList
            for ipAddr, port in walletList:
                print("Sending to "+ ipAddr + ":" + str(port))
                SocketUtils.sendObj(ipAddr, newBlock, 5006)
            headBlocks.remove(newBlock.previousBlock)
            headBlocks.append(newBlock)
    return True

if __name__ == "__main__":
    myPriv, myPubl = Signatures.generate_keys()
    t1 = threading.Thread(target = minerServer, args = (('localhost',5005),))
    t2 = threading.Thread(target = nonceFinder, args = (wallets, myPubl,))

    server = SocketUtils.newServerConnection('localhost', 5006)

    t1.start()
    t2.start()

    priv1, publ1 = Signatures.generate_keys()
    priv2, publ2 = Signatures.generate_keys()
    priv3, publ3 = Signatures.generate_keys()

    Tx1 = Transaction.Tx()
    Tx2 = Transaction.Tx()

    Tx1.add_input(publ1, 4.0)
    Tx1.add_input(publ2, 1.0)
    Tx1.add_output(publ3, 4.8)
    Tx2.add_input(publ3, 4.0)
    Tx2.add_output(publ2, 4.0)
    Tx2.add_reqd(publ1)

    Tx1.sign(priv1)
    Tx1.sign(priv2)
    Tx2.sign(priv3)
    Tx2.sign(priv1)

    try:
        SocketUtils.sendObj('localhost', Tx1)
        print("Sent Tx1")
        SocketUtils.sendObj('localhost', Tx2)
        print("Sent Tx2")
    except:
        print("Error: Connection unsuccessful")

    for i in range(30):
        newBlock = SocketUtils.recvObj(server)
        if newBlock:
            break

    if newBlock.is_valid():
       print("Success, block is valid")
    else:
        print("Error, invalid block")
    if newBlock.good_nonce():
        print("Success, nonce is valid")
    else:
        print("Error, invalid nocne")

    for tx in newBlock.data:
        try:
            if tx.inputs[0][0] == publ1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present")
        except:
            pass
        try:
            if tx.inputs[0][0] == publ3 and tx.inputs[0][1] == 4.0:
                print("Tx2 is present")  
        except:
           pass

    time.sleep(20)
    breakNow = True
    time.sleep(2)
    server.close()


    t1.join()
    t2.join()

    print("Done")