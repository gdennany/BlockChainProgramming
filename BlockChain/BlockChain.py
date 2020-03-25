from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class someClass:
    string = None
    num = 456433
    def __init__(self, mystr):
        self.string = mystr
    def __repr__(self):
        return self.string + " ^^^ " + str(self.num)

class CBlock:
    data = None
    previousHash = None
    previousBlock = None
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()
    def computeHash(self):
        hashAccumulator = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hashAccumulator.update(bytes(str(self.data), 'utf8'))           #adds hashed value of input data
        hashAccumulator.update(bytes(str(self.previousHash), 'utf8'))  #prepends previous blocks hash value to the newly hashed data
        return hashAccumulator.finalize()
    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.computeHash() == self.previousHash

if __name__ == '__main__':
    root = CBlock('I am root', None)
    Block1 = CBlock('I am a child', root)
    Block2 = CBlock(b'I am a child (and B1s brother)', root)
    Block3 = CBlock(12345, Block1)
    Block4 = CBlock(someClass('hello'), Block3)
    Block5 = CBlock('Top Block', Block4)


    for b in [Block1, Block2, Block3, Block4, Block5]:
        if (b.previousBlock.computeHash() == b.previousHash):
            print("Success, hash matches")
        else:
            print("Error, hash doesnt match")

    Block3.data = 1245
    if Block4.previousBlock.computeHash() == Block4.previousHash:
        print("Failure, couldnt detect tampering")
    else:
        print("Success, tampering detected")

    print(Block4.data)
    Block4.data.num = 99999
    print(Block4.data)
    if Block5.previousBlock.computeHash() == Block5.previousHash:
        print("Failure, couldnt detect tampering")
    else:
        print("Success, tampering detected")
        
    
