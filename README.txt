ELEC 473 Assignment 2 Option 1: Elliptic Curve ElGamal Encryption

Source Code:

encrypt_decrypt.py:
This file holds the necessary functions to perform EC-elgamal encryption and decryption on plaintext messages. The function to encrypt uses the generator G = [0x3b4c382ce37aa192a4019e763036f4f5dd4d7ebb, 0x938cf935318fdced6bc28286531733c3f03c4fee], and multiplies it by the message m to map the message to a point on the curve. Then we create Ciphertext1 or C1 which is the generator multiplied by the encrypter's random key. We then do C2 as the message point on the curve plus the key which is k^ab. The decryption algorithm finds the key by multiplying C1 by the private key, and then subtracting it from C2. When then brute force to find which integer k multiplied by the generator gives us the message mapped to a point, and the message is said integer. Some utf-8 encodings to int and vice versa are used to convert a string into an integer

473A2.py:
This is the main program that sets the parameters for the secp160k1 elliptic curve. We encrypt our plaintext character by character into it's utf-8 encoding and run the encryption function. Then we decrypt the cipher text using the decryption function.

Output Files:

generator_and_randomkey.txt: the generator and the encryptors random private key 
privatekey.txt: the decryption private key
publickey.txt: the Decrypter public key
ciphertext.txt: the cipher texts
decrypted_plaintext.txt: the decrypted plaintexts


HOW TO RUN:

Run 473A2.py
