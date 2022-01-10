import sympy
import random


def generate_large_prime():
    """
    :return: a random prime number which will be used in the RSA algorithm
    """
    current_prime = sympy.randprime(2 ** 16, 2 ** 32)
    return current_prime


def modular_multiplicative_inverse(a, mod_value):
    """
    A function to compute the modular multiplicative inverse of a number
    :param a: the number we want to compute the inverse for
    :param mod_value: the congruence class
    :return: x: the multiplicative inverse such that a * x = 1 mod mod_value
    """

    x = 0
    x0 = 1
    r = mod_value
    r0 = a

    while r0 != 0:
        quotient = r // r0
        x, x0 = x0, x - quotient * x0
        r, r0 = r0, r - quotient * r0

    if r > 1:
        return 'Input doesnt have an inverse'
    if x < 0:
        x = x + mod_value

    return x


def gcd(a, n):
    """
    A function to compute the greatest common divisor of two numbers
    :param a: number 1
    :param n: number 2
    :return: the greatest common divisor
    """

    while n != 0:
        a, n = n, a % n
    return a


def rsa_encryption(plain_text):
    """
    A function to implement the RSA algorithm, both encryption and decryption.
    :param plain_text:
    :return:
    """
    p = generate_large_prime()
    q = generate_large_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, 2 ** 32)
    while True:
        if gcd(phi, e) == 1 and e < phi:  # phi and e must be co-prime and e < phi
            break
        e = random.randint(2, 2 ** 32)

    d = modular_multiplicative_inverse(e, phi)

    encrypted_text = pow(plain_text, e, n)

    plain_text_from_encrypted_text = pow(encrypted_text, d, n)

    print("Plain text: " + str(plain_text))
    print("Encrypted text: " + str(encrypted_text))
    print("Decrypted text: " + str(plain_text_from_encrypted_text))
    print("\n\n")
    return encrypted_text, d, e
