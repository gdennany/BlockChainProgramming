from BlockChain import CBlock
from Signatures import generate_keys, sign, verify
from Transaction import Tx
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import time
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

blockReward = 25.0
leadingZeros = 2        #number of leading zeros miners need to produce to satisfy new block 
nextCharLimit = 20

class TxBlock (CBlock):
    nonce = "XXXXXXX"
    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)
    
    def addTx (self, Tx_in):
        self.data.append(Tx_in)
    
    def __count_totals(self):
        totalIn = 0
        totalOut = 0
        for tx in self.data:
            for addr, amount in tx.inputs:
                totalIn = totalIn + amount
            for addr, amount in tx.outputs:
                totalOut = totalOut + amount
        return (totalIn, totalOut)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        totalIn, totalOut = self.__count_totals()
        #if totalOut > (totalIn + blockReward):
        if totalOut - totalIn - blockReward > 0.000000000001:   #fix floating point error bug
            return False
        return True

    def good_nonce(self):
        hashAccumulator = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hashAccumulator.update(bytes(str(self.data), 'utf8'))           #adds hashed value of input data
        hashAccumulator.update(bytes(str(self.previousHash), 'utf8'))  #prepends previous blocks hash value to the newly hashed data
        hashAccumulator.update(bytes(str(self.nonce), 'utf-8'))         #add nonce to hashing operation
        currentHash = hashAccumulator.finalize()
        #print(currentHash[:leadingZeros])
        
        
        if currentHash[: leadingZeros] != bytes(''.join([ '\x00' for i in range(leadingZeros)]), 'utf-8'):
            return False

        return int(currentHash[leadingZeros]) < nextCharLimit

    def find_nonce(self):
        for i in range(1000000):
            self.nonce = ''.join([ 
                    chr(random.randint(0, 255)) for i in range(10 * leadingZeros)])
            if self.good_nonce():
                return self.nonce

        return None
    

if __name__ == '__main__':
    priv1, publ1 = generate_keys()
    priv2, publ2 = generate_keys()
    priv3, publ3 = generate_keys()
    priv4, publ4 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(publ1, 1)
    Tx1.add_output(publ2, 1)
    Tx1.sign(priv1)

    if Tx1.is_valid():
        print("Succesful transaction")
    else:
        print("Error: Invalid Transaction")
 
    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    newTx = pickle.load(loadfile)

    if newTx.is_valid():
        print("Succesful transaction")
    else:
        print("Error: Invalid Transaction")
    loadfile.close()
    
    
    root = TxBlock(None)
    root.addTx(Tx1)

    Tx2 = Tx()
    Tx2.add_input(publ2, 1.1)
    Tx2.add_output(publ3, 1)
    Tx2.sign(priv2)
    root.addTx(Tx2)

    Block1 = TxBlock(root)
    Tx3 = Tx()
    Tx3.add_input(publ3, 1.1)
    Tx3.add_output(publ1, 1)
    Tx3.sign(priv3)
    Block1.addTx(Tx3)

    Tx4 = Tx()
    Tx4.add_input(publ1, 1)
    Tx4.add_output(publ2, 1)
    Tx4.add_reqd(publ3)
    Tx4.sign(priv1)
    Tx4.sign(priv3)
    Block1.addTx(Tx4)
    start = time.time()
    print(Block1.find_nonce())
    elapsed = time.time() - start
    print("Elapsed time: " + str(elapsed) + " seconds")
    if elapsed < 60:
        print("Error, mining is too fast")
    if Block1.good_nonce():
        print("Success, Nonce is good")
    else:
        print("Error, bad nonce")
    
    Block1.is_valid()
    root.is_valid()

    savefile = open("block.dat", "wb")
    pickle.dump(Block1, savefile)
    savefile.close()

    loadfile = open("block.dat", "rb")
    load_Block1 = pickle.load(loadfile)

    load_Block1.is_valid()

    for b in [root, Block1, load_Block1, load_Block1.previousBlock]:
        if b.is_valid():
            print("Success, valid block")
        else:
            print("Error, bad block")

    if Block1.good_nonce():
        print("Success, Nonce is good after save and load")
    else:
        print("Error, bad nonce after load")

    #Testing invalid blocks
    Block2 = TxBlock(Block1)
    Tx5 = Tx()
    Tx5.add_input(publ3, 1)
    Tx5.add_output(publ1, 100)
    Tx5.sign(priv3)
    Block2.addTx(Tx5)

    load_Block1.previousBlock.addTx(Tx4)

    for b in [Block2, load_Block1]:
        if b.is_valid():
            print("Error: bad block undetected")
        else:
            print("Success, bad block detected")


    #Test mining rewards and transaction fees
    Block3 = TxBlock(Block2)
    Block3.addTx(Tx2)
    Block3.addTx(Tx3)
    Block3.addTx(Tx4)
    Tx6 = Tx()
    #miner gets reward and adds 25 new coins to their wallet (public key)
    Tx6.add_output(publ4, 25)
    Block3.addTx(Tx6)
    if Block3.is_valid():
        print("Success, block rewarded successfully")
    else: 
        print("Error, block reward failed")

    #Miner takes transaction fees (incentive for miners to put someone elses transaction onto their block)
    Block4 = TxBlock(Block3)
    Block4.addTx(Tx2)
    Block4.addTx(Tx3)
    Block4.addTx(Tx4)
    Tx7 = Tx()
    Tx7.add_output(publ4, 25.2)
    Block4.addTx(Tx7)
    if Block4.is_valid():
        print("Success, transaction fee rewarded successfully")
    else: 
        print("Error, transaction fee reward failed")

    #test Greedy miner trying to add more to wallet than deserves
    Block5 = TxBlock(Block4)
    Block5.addTx(Tx2)
    Block5.addTx(Tx3)
    Block5.addTx(Tx4)
    Tx8 = Tx()
    Tx8.add_output(publ4, 26)
    Block5.addTx(Tx8)
    if not Block5.is_valid():
        print("Success, greedy miner detected")
    else: 
        print("Error, greedy miner not detected")

