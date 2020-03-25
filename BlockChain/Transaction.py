from Signatures import generate_keys

#Tx abbreviate transaction
class Tx:
    inputs = None     #list of input address
    outputs = None    #list of output addresses and amounts
    sigs = None       #list of signatures
    reqd = None       #list of required signatures that are not inputs (to facilitate escrow transactions)
    def __init__(self):
        inputs = []
        outputs = []
        sigs = []
        reqd = []
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
    priv1, publ1 = generate_keys()  #defined in signatures class
    priv2, publ2 = generate_keys()
    priv3, publ3 = generate_keys()
    priv4, publ4 = generate_keys()

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
    Tx3.sign(priv3)

    #Test valid transactions
    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Successful transaction")
        else:
            print("Failed transaction")

    #Test invalid transactions
    for t in [Tx4]:
        if t.is_valid():
            print("Successful transaction")
        else:
            print("Failed transaction")    
    