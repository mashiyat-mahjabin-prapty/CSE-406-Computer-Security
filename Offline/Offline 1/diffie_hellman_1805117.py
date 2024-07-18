# miller rabin primality test
import random
import time
from statistics import mean

time_matrix = [[[0 for i in range(5)] for j in range(6)] for k in range(3)]

# utility function to do modular exponentiation
# It returns (x^y) % p
def power(x, y, p):
    result = 1
    x = x % p
    while (y > 0):
        if ((y & 1) == 1):
            result = (result * x) % p
        y = y >> 1
        x = (x * x) % p
    return result
# This function is called for all k trials. It returns
# false if n is composite and returns false if n is
# probably prime.
# d is an odd number such that d*2<sup>r</sup> = n-1
# for some r >= 1
def millerTest(d, n):
    a = 2 + random.randint(1, n - 4)
    x = power(a, d, n)
    if (x == 1 or x == n - 1):
        return True
    while (d != n - 1):
        x = (x * x) % n
        d *= 2
        if (x == 1):
            return False
        if (x == n - 1):
            return True
    return False
# It returns false if n is composite and returns true if n
# is probably prime. k is an input parameter that determines
# accuracy level. Higher value of k indicates more accuracy.
def isPrime(n, k):
    # Corner cases
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True
    # Find r such that n = 2^d * r + 1 for some r >= 1
    d = n - 1
    while (d % 2 == 0):
        d //= 2
    # Iterate given nber of 'k' times
    for i in range(k):
        if (millerTest(d, n) == False):
            return False
    return True 
# This code is contributed by mits
# https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/

# random k bit prime generator
def random_prime(l):
    while True:
        p = random.randint(2**(l-1), 2**l-1)
        if isPrime(p, 10):
            return p

# primitive root generator
def primitive_root(p):
    while True:
        g = random.randint(2, p-1)
        if pow(g, (p-1)//2, p) != 1:
            if pow(g, (p-1)//3, p) != 1:
                return g

# get the value of s
def get_s(B, a, p):
    s = pow(B, a, p)
    return s

def generate_a(l):
    a = random_prime(l//2+1)
    return a

def generate_b(l):
    b = random_prime(l//2+1)
    return b

def generate_B(g, b, p):
    B = pow(g, b, p)
    return B

def generate_A(g, a, p):
    A = pow(g, a, p)
    return A

# Diffie-Hellman key exchange
def diffie_hellman(l):
    t1 = time.time()
    p = random_prime(l)
    t2 = time.time()
    # make first and last bits of p as 1
    p = p | (1 << (l-1))
    p = p | 1
    g = primitive_root(p)
    t3 = time.time()
    a = random_prime(l//2+1)
    b = random_prime(l//2+1)
    t4 = time.time()
    A = power(g, a, p)
    B = power(g, b, p)
    t5 = time.time()
    s1 = power(B, a, p)
    s2 = power(A, b, p)
    if s1 == s2:
        t6 = time.time()
        return s1
    else:
        return False

def diffie_hellman_with_time(index, l):
    # print('For ', l, ' bits(in dh):')
    for i in range(5):
        t1 = time.time()
        p = random_prime(l)
        t2 = time.time()
        # make first and last bits of p as 1
        p = p | (1 << (l-1))
        p = p | 1
        g = primitive_root(p)
        t3 = time.time()
        a = random_prime(l//2+1)
        b = random_prime(l//2+1)
        t4 = time.time()
        A = power(g, a, p)
        B = power(g, b, p)
        t5 = time.time()
        s1 = power(B, a, p)
        s2 = power(A, b, p)
        if s1 == s2:
            t6 = time.time()
            time_matrix[index][0][i] = t2-t1
            time_matrix[index][1][i] = t3-t2
            time_matrix[index][2][i] = (t4-t3)/2.0
            time_matrix[index][3][i] = (t5-t4)/2.0
            time_matrix[index][4][i] = (t6-t5)/2.0
            return s1
        else:
            return False

# test
def main():
    # k = int(input('Enter the number of bits: '))
    bit = [128, 192, 256]
    for i in range(len(bit)):
        print('For ', bit[i], ' bits:')
        print(diffie_hellman_with_time(i, bit[i]))
        print()
        print('Time Statistics')
        print('Time taken to determine p: ', mean(time_matrix[i][0]), 'seconds')
        print('Time taken to determine g: ', mean(time_matrix[i][1]), 'seconds')
        print('Time taken to determine a/b: ', mean(time_matrix[i][2]), 'seconds')
        print('Time taken to determine A/B: ', mean(time_matrix[i][3]), 'seconds')
        print('Time taken to determine s: ', mean(time_matrix[i][4]), 'seconds')    
        print()

if __name__ == '__main__':
    main()