#!/usr/bin/env python
# -*- coding: cp1252 -*-
import sys
import random, math
has_pycryptodome = True
try:
    from Crypto.Util import number
except ImportError:
    has_pycryptodome = False

key_length = 5
e_stored = 3
n_stored = 901
d_stored = 555
encrypted_msg_stored = ''

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
    if has_pycryptodome:
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
    else:
        print('The pycryptodome libery is needed for this function.')
        print('It can be installed with: "pip install pycryptodome".')


def crypt(msg,a,b):
    # convert numbers in list to bit and add to string
    msg = ''.join([format(ord(x), '08b') for x in msg])

    msgBit10Int = []
    for i in range(math.ceil(len(msg)/10)):
        msgBit10Int.append(int(msg[:10].ljust(10,'0'),2))
        msg = msg[10:]
    crypted_msg = ''.join([format(pow(x,a,b), '010b') for x in msgBit10Int])
    msgBit8Int = []
    for i in range(math.floor(len(crypted_msg)/8)):
        msgBit8Int.append(chr(int(crypted_msg[:8],2)))
        crypted_msg = crypted_msg[8:]
    crypted_msg = ''.join([str(x) for x in msgBit8Int])
    return crypted_msg

def encrypt():
    e = e_stored
    n = n_stored
    if e is not None and n is not None:
        if input('Use stored key?(y/n)\n') != 'y':
            e = input('Enter Private Key e')
            n = input('Enter Private Key n')
    else:
        e = input('Enter Private Key e')
        n = input('Enter Private Key n')

    msg = input('Enter message\n')

    encrypted_msg  = crypt(msg,e,n)
    print('Encrypted Message:')
    print(encrypted_msg)

    if input('Store message(n/y)\n') == 'y':
        global encrypted_msg_stored

        encrypted_msg_stored = encrypted_msg
        print('Message Saved')

def decrypt():
    d = d_stored
    n = n_stored
    if d is not None and n is not None:
        if input('Use stored key?(y/n)\n') != 'y':
            e = input('Enter Public Key d')
            n = input('Enter Public Key n')
    else:
        e = input('Enter Public Key d')
        n = input('Enter Public Key n')

    if encrypted_msg_stored != '':
        if input('Use stored message(n/y)\n') == 'y':

            msg = encrypted_msg_stored
    else:
        msg = input('Enter message\n')

    decrypted_msg = crypt(msg,d,n)
    print('Decrypted Message:')
    print(decrypted_msg)

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
