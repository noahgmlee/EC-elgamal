#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 14:07:19 2022

@author: noahlee
"""

from encrypt_decrypt import encrypt_data, decrypt_data, doubleAndAdd

p = 11
a = 1
b = 6
G = [2, 7] #generator
Ord = 13

decrypter_private_key = 4
decrypter_public_key = doubleAndAdd(G[0], G[1], decrypter_private_key, a, b, p)

encrypter_random_key = 7

PTs = [5, 3, 9]
index = 1
for PT in PTs:
    PTasInt = PT
    CT = encrypt_data(G, encrypter_random_key, decrypter_public_key, PTasInt, a, b, p)
    Decipher = decrypt_data(decrypter_private_key, CT, a, b, p, G, Ord)
    print ("\nDeciphered int is:")
    print (Decipher)

    
