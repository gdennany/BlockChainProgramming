# Used website cryptography.io => Primitives => Authenticate encryption => Asymmetric Algorithms => RSA


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,     
        backend=default_backend())

    public_key = private_key.public_key()

    public_key_serialized = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    return private_key, public_key_serialized


def sign(message, private_key):
    message = bytes(str(message), 'utf-8')
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
    return signature

def verify(message, signature, public_key_serialized):

    public_key = serialization.load_pem_public_key(
         public_key_serialized,
         backend=default_backend()
     )

    message = bytes(str(message), 'utf-8')
    try:
        public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
            )
        return True
    except InvalidSignature:
        return False
    except:
        print("Error executing public_key.verify")
    return False


if __name__ == '__main__':
    priv, publ = generate_keys()
    message = b'This is a secret message'   #b makes this a byte representation of the string
    sig = sign(message, priv)
    correct = verify(message, sig, publ)

    if correct:
        print("Success, good signature")
    else:
        print("Error, bad signature")

    priv1, publ1 = generate_keys()
    sig1 = sign(message, priv1)
    correct = verify(message, sig1, publ)
    if correct:
        print("Error: bad signature passes")
    else:
        print("Success, bad signature detected")

    badmessage = message + b"Q"
    correct = verify(badmessage, sig, publ)
    if correct:
        print("Error: bad message passes")
    else:
        print("Success, bad message (tampering) detected")

    priv2, publ2 = generate_keys()
    sig2 = sign(badmessage, priv2)
    correct = verify(badmessage, sig2, publ2)
    if correct:
        print("Success, good signature")
    else:
        print("Error, bad signature")
