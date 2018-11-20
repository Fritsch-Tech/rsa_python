#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random
from Crypto.Util import number
key_length = 50
e_stored = 450364575923581272008315327707
n_stored = 533739451994951398578128257201
d_stored = 68829681578788613803668547507

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def print_optiones():
    print('Operationes:')
    print('h Help')
    print('g Generate Key')
    print('p Print Keys')
    print('e Encrypt message')
    print('d decrypt message')
    print('q Exit')

def stop():
    print('Goodbye')
    sys.exit(0)

def generate_keys():
    p = number.getPrime(key_length)
    q = number.getPrime(key_length)
    n = p*q
    phi = (p - 1)*(q - 1)
    e = number.getPrime(n.bit_length())
    while e < 1 or e > n:
        e = number.getPrime(n.bit_length())

    d = modinv(e,phi)

    print('Public Key: \t {}  {}'.format(e,n))
    print('Private Key: \t {}  {}'.format(d,n))
    if input('Store Keys(n/y)\n') == 'y':
        global e_stored
        global n_stored
        global d_stored

        e_stored = e
        n_stored = n
        d_stored = d
        print('Keys Saved')


def encrypt():
    e = e_stored
    n = n_stored
    if e is not None and n is not None:
        if input('Use saved key?(y/n)\n') != 'y':
            e = input('Enter Private Key e')
            n = input('Enter Private Key n')
    else:
        e = input('Enter Private Key e')
        n = input('Enter Private Key n')

    msg = input('Enter message\n')
    encrypted_msg = []
    for char in msg:
        encrypted_msg.append(pow(ord(char),e,n))
    print(encrypted_msg)
    for b in encrypted_msg:
        print(chr(pow(b,d_stored,n_stored)))
def decrypt():
    d = d_stored
    n = n_stored
    if d is not None and n is not None:
        if input('Use saved key?(y/n)\n') != 'y':
            e = input('Enter Public Key d')
            n = input('Enter Public Key n')
    else:
        e = input('Enter Public Key d')
        n = input('Enter Public Key n')

    msg = input('Enter message\n')
    print(chr(pow(int(msg),d,n)))

def operation_not_found():
    print('unknown operation')

def print_keys():
    if n_stored is not None and e_stored is not None:
        print('Public key: \n e={} \n n={}'.format(e_stored,n_stored))
    else:
        print('No public key saved')

    if n_stored is not None and d_stored is not None:
        print('Private key: \n d={} \n n={}'.format(d_stored,n_stored))
    else:
        print('No public key saved')

operationes = {
    'g':generate_keys,
    'h':print_optiones,
    'q':stop,
    'p':print_keys,
    'e':encrypt,
    'd':decrypt
}

def main():
    print('RSA encrypt/decrypt')
    print_optiones()
    print('____________')
    while True:
        operation = operationes.get(input(),operation_not_found)
        operation()
        print('____________')

if __name__ == '__main__':
    main()
