import SocketUtils
import Transaction
import TxBlock
import Signatures

wallets = ['localhost']
txList = []
headBlocks = [None]

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

def minerServer(myIP, walletList, myPublic):
    #Open Server Connection
    server = SocketUtils.newServerConnection('localhost')
    #recieve two transactions wallet
    for i in range(10):
        print("Finding Nonce...")
        newTx = SocketUtils.recvObj(server)
        if isinstance(newTx, Transaction.Tx):
            txList.append(newTx)
            print("Recieved Tx")
        if len(txList) >= 2:
            break
    
    #collect those transactions into a block
    newBlock = TxBlock.TxBlock(findLongestBlockChain())
    newBlock.addTx(txList[0])
    newBlock.addTx(txList[1])
    
    #compute and add mining reward
    totalIn, totalOut = newBlock.count_totals()
    mineReward = Transaction.Tx()
    mineReward.add_output(myPublic, 25.0 + totalIn - totalOut)
    newBlock.addTx(mineReward)
    
    #Mine (i.e. find a satisfying nonce)
    for i in range(10):
        newBlock.find_nonce()
        if newBlock.good_nonce():
            print("Good nonce found")
            break
    if not newBlock.good_nonce():
        print("Error: Couldnt find satisfying nonce")
        return False
    
    #send that new block to each in walletList
    for ipAddr in walletList:
        print("Sending to "+ ipAddr)
        SocketUtils.sendObj(ipAddr, newBlock, 5006)
    headBlocks.remove(newBlock.previousBlock)
    headBlocks.append(newBlock)
    return False

myPriv, myPubl = Signatures.generate_keys()
minerServer('localhost', wallets, myPubl)