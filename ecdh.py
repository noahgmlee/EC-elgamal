#!/usr/bin/python3

#MrMouseMath ECDH algorithm implementation

from encrypt_decrypt import pt_to_point, encrypt_data, decrypt_data, doubleAndAdd
import random

#Helper functions inspired by https://github.com/serengil/crypto/blob/d0520d85951e4c3808d13012bd5fe1b9a70dcf7d/python/EC-ElGamal.py#L6
def PTtoInt(PT):
    PT_encoded = PT.encode('utf-8')
    PT_hex = PT_encoded.hex()
    PT_int = int(PT_hex, 16)
    return PT_int

def intToPT(PTasInt):
    import codecs
    PTasHex = hex(PTasInt)
    PTasHex = PTasHex[2:]
    return codecs.decode(codecs.decode(PTasHex,'hex'),'utf-8')


#pick an eliptic curve
#Using secp160k1 from https://neuromancer.sk/std/secg/secp160k1
#y = x^3 + ax + b
p = 0xfffffffffffffffffffffffffffffffeffffac73
a = 0
b = 7
G = [0x3b4c382ce37aa192a4019e763036f4f5dd4d7ebb, 0x938cf935318fdced6bc28286531733c3f03c4fee] #generator
Ord = 0x0100000000000000000001b8fa16dfab9aca16b6b3

decrypter_private_key = random.getrandbits(160)
while (decrypter_private_key > Ord):
    decrypter_private_key = random.getrandbits(160)
decrypter_public_key = doubleAndAdd(G[0], G[1], decrypter_private_key, a, b, p)

encrypter_random_key = random.getrandbits(160)
while (encrypter_random_key > Ord):
    encrypter_random_key = random.getrandbits(160)

PT = ""
while PT != "exit":
    PT = input("Enter the plaintext to be encrypted: ")
    PTcharArr = list(PT)
    CT = []
    for i in PTcharArr:
        PTasInt = PTtoInt(i)
        CT.append(encrypt_data(G,
                               encrypter_random_key,
                               decrypter_public_key,
                               pt_to_point(PTasInt, a, b, p),
                               a,
                               b,
                               p))
    print(CT)
    input("hit enter when ready to decrypt")
    DecipherText = []
    for point in CT:
        Decipher = decrypt_data(decrypter_private_key, point, a, b, p, G, Ord)
        DecipherText.append(intToPT(Decipher))
    print(DecipherText)
