#define "Point at Infinity"
PatInf = [0, 0]

#exponentiation by squaring
def pow1(base, exponent, modulus):
    result = 1
    base = base % modulus
    while (exponent > 0):
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = int(exponent) >> 1
        base = (base * base) % modulus
    return result

def isQuadraticResidue(y, p):
    if pow1(y, (p - 1)/2, p) == p-1:
        return False
    else:
        return True

#Take PT and curve parameters. return point on curve
def pt_to_point(pt, a, b, p):
    num_try_bits = 8
    l = 0
    x = (pt << 8)
    y = 0
    while (l < (2**num_try_bits - 1)):
        y_sqr = (x**3 + a*x + b) % p
        if isQuadraticResidue(y_sqr, p):
            y = pow1(y_sqr, (p+1)/4, p)
            print("SUCCESS!!!!!!")
            break
        else:
            print("try")
            l = l + 1
            x = x | l
    return [x, y]

def encrypt_data(g, random_key, public_key, m, a, b, p):
    print ("\nENCRYPTING DATA!!\n")
    #PTasPoint = doubleAndAdd(g[0], g[1], m, a, b, p)
    print ("\nPT point: ")
    print (m)
    C1 = doubleAndAdd(g[0], g[1], random_key, a, b, p)
    C2 = doubleAndAdd(public_key[0], public_key[1], random_key, a, b, p)
    print ("\nEncrypting Key point: ")
    print (C2)
    C2 = add_points(C2[0], C2[1], m[0], m[1], a, b, p)
    print ("\nCipher Point is: ")
    print (C2)
    return [C1,C2]

def decrypt_data(private_key, C, a, b, p, g, Ord):
    print ('\nDECRYPTING DATA!!\n')
    ay1 = doubleAndAdd(C[0][0], C[0][1], private_key, a, b, p)
    print ("\nay1 is: ")
    print (ay1)
    decipherAsPoint = add_points(C[1][0], C[1][1], ay1[0], ay1[1]*-1, a, b, p)
    print ("\nDeciphered point is: ")
    print (decipherAsPoint)
    tempPoint = g
    decipherAsInt = decipherAsPoint[0] >> 8
    return decipherAsInt

def add_points(x0, y0, x1, y1, a, b, p):
    while x0 < 0:
        x0 = x0 + p

    while y0 < 0:
        y0 = y0 + p

    while x1 < 0:
        x1 = x1 + p

    while y1 < 0:
        y1 = y1 + p

    if x0 == x1 and y0 == y1: #this means we apply the doubling equations
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

    x2 = (Lambda*Lambda - x0 - x1) % p
    y2 = ((x0 - x2)*Lambda - y0) % p

    return x2, y2

#double and add method from wikipedia https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
def doubleAndAdd(Gx, Gy, k, a, b, p):
    res_x = 0
    res_y = 0

    temp_x = Gx
    temp_y = Gy

    kAsBinary = bin(k) #0b1111111001
    kAsBinaryNoMSB = kAsBinary[2:len(kAsBinary)] #1111111001
    for bit in reversed(kAsBinaryNoMSB):
        if bit == '1':
            res_x, res_y = add_points(res_x, res_y, temp_x, temp_y, a, b, p)
        temp_x, temp_y = add_points(temp_x, temp_y, temp_x, temp_y, a, b, p)
    return res_x, res_y

def mod_inv(a, m):
    return pow(a, -1, m)
