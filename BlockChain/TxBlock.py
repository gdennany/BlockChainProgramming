from BlockChain import CBlock
from Signatures import generate_keys, sign, verify
from Transaction import Tx
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class TxBlock (CBlock):
    
    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)
    def addTx (self, Tx_in):
        self.data.append(Tx_in)
    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        return True

if __name__ == '__main__':
    priv1, publ1 = generate_keys()
    priv2, publ2 = generate_keys()
    priv3, publ3 = generate_keys()

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

