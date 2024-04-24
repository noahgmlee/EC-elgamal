
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 14:07:19 2022

@author: noahlee
"""

from encrypt_decrypt import encrypt_data, decrypt_data, doubleAndAdd
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

GnR_file = open('generator_and_randomkey.txt', 'w')
GnR_file.writelines("Generator: " + str(G) + '\n')

decrypter_private_key = random.getrandbits(160)
if decrypter_private_key > Ord:
    decrypter_private_key = Ord - 1
decrypter_public_key = doubleAndAdd(G[0], G[1], decrypter_private_key, a, b, p)
SK_file = open('privatekey.txt', 'w')
SK_file.writelines(str(decrypter_private_key))
SK_file.close()

PK_file = open('publickey.txt', 'w')
PK_file.writelines(str(decrypter_public_key))
PK_file.close()

encrypter_random_key = random.getrandbits(160)
if encrypter_random_key > Ord:
    encrypter_random_key = Ord - 1

GnR_file.writelines("Random Encryption Key: " + str(encrypter_random_key))
GnR_file.close()

PTs = ["I am an undergraduate student at queen’s university.", "Noah Graeme Matthew Lee"]
CT_file = open('ciphertext.txt', 'w')
Decipher_file = open('decrypted_plaintext.txt', 'w')
index = 1
for PT in PTs:
    PTcharArr = list(PT)
    CT_file.writelines("CipherText" + str(index) + ": \n")
    Decipher_file.writelines("Decrypted Plain Text" + str(index) + ": \n")
    for i in PTcharArr:
        PTasInt = PTtoInt(i)
        print("\nInput Int is:")
        print(PTasInt)
        CT = encrypt_data(G, encrypter_random_key, decrypter_public_key, PTasInt, a, b, p)
        Decipher = decrypt_data(decrypter_private_key, CT, a, b, p, G, Ord)
        DecipherAsText = intToPT(Decipher)
        print("\nDeciphered Int and Text is:")
        print(Decipher)
        print(DecipherAsText)
        CT_file.writelines(str(CT) + '\n')
        Decipher_file.writelines(DecipherAsText)
    Decipher_file.writelines('\n')
    index = index + 1

CT_file.close()
Decipher_file.close()
    
