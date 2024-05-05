#define "Point at Infinity"
PatInf = [0, 0]

#exponentiation by squaring
def fastPow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while (exponent > 0):
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = int(exponent) >> 2
        base = (base * base) % modulus
    return result

#cofactor of 1 just check if point is a quad res
#p is congruent to 3 mod 4
def isQuadraticResidue(y, p):
    if fastPow(y, (p - 1)/2, p) == p-1:
        return False
    else:
        return True

#Take PT and curve parameters. return point on curve
def pt_to_point(pt, a, b, p):
    num_try_bits = 8
    l = 0
    x = (pt << num_try_bits)
    y = 0
    while (l < (2**num_try_bits - 1)):
        y_sqr = (x**3 + a*x + b) % p
        if isQuadraticResidue(y_sqr, p):
            y = fastPow(y_sqr, (p+1)/4, p)
            break
        else:
            l = l + 1
            x = x | l
    return [x, y]

def encrypt_data(g, random_key, public_key, m, a, p):
    print ("\nENCRYPTING DATA!!\n")
    print ("\nPT point: ")
    print (m)
    C1 = doubleAndAdd(g[0], g[1], random_key, a, p)
    C2 = doubleAndAdd(public_key[0], public_key[1], random_key, a, p)
    print ("\nEncrypting Key point: ")
    print (C2)
    C2 = add_points(C2[0], C2[1], m[0], m[1], a, p)
    print ("\nCipher Point is: ")
    print (C2)
    return [C1,C2]

def decrypt_data(private_key, C, a, p):
    print ('\nDECRYPTING DATA!!\n')
    ay1 = doubleAndAdd(C[0][0], C[0][1], private_key, a, p)
    print ("\nay1 is: ")
    print (ay1)
    decipherAsPoint = add_points(C[1][0], C[1][1], ay1[0], ay1[1]*-1, a, p)
    print ("\nDeciphered point is: ")
    print (decipherAsPoint)
    decipherAsInt = decipherAsPoint[0] >> 8
    return decipherAsInt

def add_points(x0, y0, x1, y1, a, p):
    while y1 < 0:
        y1 = y1 + p

    if x0 == x1 and y0 == y1:
        Lambda = (3*x0*x0 + a) * mod_inv(2*y0, p)
    else:
        if x0 == x1:
            return PatInf
        elif [x0, y0] == PatInf:
            return x1, y1
        elif [x1, y1] == PatInf:
            return x0, y0
        else:
            Lambda = (y1 - y0) * mod_inv(x1 - x0, p)

    x2 = (Lambda * Lambda - x0 - x1) % p
    y2 = ((x0 - x2) * Lambda - y0) % p
    return x2, y2

#double and add method from wikipedia https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
def doubleAndAdd(Gx, Gy, k, a, p):
    res = PatInf
    temp = [Gx, Gy]

    kAsBinary = bin(k) #0b101010101
    kAsBinary = kAsBinary[2:len(kAsBinary)]
    for bit in reversed(kAsBinary):
        if bit == '1':
            res = add_points(res[0], res[1], temp[0], temp[1], a, p)
        temp = add_points(temp[0], temp[1], temp[0], temp[1], a, p)
    return res

def mod_inv(a, m):
    return pow(a, -1, m) #since python 3.8 (demonstrated in last video with extended euclidean in C)
