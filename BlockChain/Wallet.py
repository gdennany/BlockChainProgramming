import SocketUtils
import Transaction
import Signatures

priv1, publ1 = Signatures.generate_keys()
priv2, publ2 = Signatures.generate_keys()
priv3, publ3 = Signatures.generate_keys()

Tx1 = Transaction.Tx()
Tx2 = Transaction.Tx()

Tx1.add_input(publ1, 4.0)
Tx1.add_input(publ2, 1.0)
Tx1.add_input(publ3, 4.8)
Tx2.add_input(publ3, 4.0)
Tx2.add_output(publ2, 4.0)
Tx2.add_reqd(publ1)

Tx1.sign(priv1)
Tx1.sign(priv2)
Tx2.sign(priv3)
Tx2.sign(priv1)

try:
    SocketUtils.sendObj('localhost', Tx1)
    SocketUtils.sendObj('localhost', Tx2)
except:
    print("Error: Connection unsuccessful")

server = SocketUtils.newServerConnection('localhost')
for i in range(10):
    newBlock = SocketUtils.recvObj(server)
    if newBlock:
        break
server.close()

if newBlock.is_valid():
    print("Success, block is valid")
else:
    print("Error, invalid block")
if newBlock.good_nonce():
    print("Success, nonce is valid")
else:
    print("Error, invalid nocne")

for tx in newBlock.data:
    if tx == Tx1:
        print("Tx1 is present")
    if tx == Tx2:
        print("Tx2 is present")    