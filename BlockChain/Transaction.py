import Signatures

#Tx abbreviate transaction
class Tx:
    inputs = None     #list of input address
    outputs = None    #list of output addresses and amounts
    sigs = None       #list of signatures
    reqd = None       #list of required signatures that are not inputs (to facilitate escrow transactions)
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
    def add_input(self, from_addr, amount):
        pass
    def add_output(self, to_addr, amount):
        pass
    def add_reqd(self, addr):
        pass
    def sign(self, privateKey):
        pass
    def is_valid(self):
        return False


if __name__ == '__main__':
    priv1, publ1 = Signatures.generate_keys()  #defined in signatures class
    priv2, publ2 = Signatures.generate_keys()
    priv3, publ3 = Signatures.generate_keys()
    priv4, publ4 = Signatures.generate_keys()

    #Testing valid transactions
    #Transaction 1: user 1 sends one keys from his public key (publ1) to the public key of user 2 (publ2) and signs the transaction
    Tx1 = Tx()
    Tx1.add_input(publ1, 1)
    Tx1.add_output(publ2, 1)
    Tx1.sign(priv1)

    Tx2 = Tx()
    Tx2.add_input(publ1, 2)
    Tx2.add_output(publ2, 1)
    Tx2.add_output(publ2, 1)

    Tx3 = Tx()
    Tx3.add_input(publ3, 1.2)
    Tx3.add_output(publ1, 1.1)
    Tx3.add_reqd(publ4)         #test escrow transactions
    Tx3.sign(priv3)
    Tx3.sign(priv4)             #third pary must also sign in escrow transactions

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Successful transaction")
        else:
            print("Error: Failed transaction")


    #Testing invalid transactions
    #Test invalid signature
    Tx4 = Tx()
    Tx4.add_input(publ1, 1)
    Tx4.add_output(publ2, 1)
    Tx4.sign(priv2)

    #Test escrow transaction not signed by the third party (should fail)
    Tx5 = Tx()
    Tx5.add_input(publ3, 1.2)
    Tx5.add_output(publ1, 1.1)
    Tx5.add_reqd(publ4)         #test escrow transactions
    Tx5.sign(priv3)
    #Tx3.sign(priv4)            #third party doesnt sign => is invalid

    #Test two input addresses, but only one signs it
    Tx6 = Tx()
    Tx6.add_input(publ3, 1)
    Tx6.add_input(publ4, .1)
    Tx6.add_output(publ1, 1.1)
    Tx6.sign(priv3)             #only one person signs => should be invalid

    #Test Outputs exceeding the input
    Tx7 = Tx()
    Tx7.add_input(publ4, 1.2)
    Tx7.add_output(publ1, 1)
    Tx7.add_output(publ2, 2)
    Tx7.sign(priv4)

    #Test negative values
    Tx8 = Tx()
    Tx8.add_input(publ2, -1)
    Tx8.add_output(publ1, -1)
    Tx8.sign(priv2)

    #A transaction that has been modified
    Tx9 = Tx()
    Tx9.add_input(publ1, 1)
    Tx9.add_output(publ2, 1)
    Tx9.sign(priv1)
    Tx9.outputs[0] = (publ3, 1)

    for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx9]:
        if t.is_valid():
            print("Error: Bad transaction passed")
        else:
            print("Success: Bad Transaction detected") 
    

