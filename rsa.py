#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random, math
from Crypto.Util import number
key_length = 5
e_stored = 3
n_stored = 901
d_stored = 555

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
    #print([elem.encode("hex") for elem in msg])

    # prepare msg for encryption

    # convert msg to 8-Bit ascii Bytes
    msg = ''.join([format(x, '08b') for x in msg.encode('ascii')])

    # join 8-Bit to 10-Bit and padd with zeros at the end
    msgBit10Int = []
    for i in range(math.ceil(len(msg)/10)):
        msgBit10Int.append(int(msg[:10].ljust(10,'0'),2))
        msg = msg[10:]

    # encrypt msg
    encrypted_msg = ''.join([format(pow(x,e,n), '010b') for x in msgBit10Int])


    msgBit8Int = []
    for i in range(math.floor(len(encrypted_msg)/8)):
        msgBit8Int.append(int(encrypted_msg[:8],2))
        encrypted_msg = encrypted_msg[8:]

    encrypted_msg  = msgBit8Int
    print('Encrypted Message:')
    for number in encrypted_msg:
        print(number,end=' ')
    print('')

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
    # convert msg to list
    msg = [int(x) for x in msg.split(' ') if x != '']

    # convert numbers in list to bit and add to string
    msg = ''.join([format(x, '08b') for x in msg])


    msgBit10Int = []
    for i in range(math.ceil(len(msg)/10)):
        msgBit10Int.append(int(msg[:10].ljust(10,'0'),2))
        msg = msg[10:]
    print(msgBit10Int)

    decrypted_msg = ''.join([format(pow(x,d,n), '010b') for x in msgBit10Int])

    msgBit8Int = []
    for i in range(math.floor(len(decrypted_msg)/8)):
        msgBit8Int.append(chr(int(decrypted_msg[:8],2)))
        decrypted_msg = decrypted_msg[8:]


    decrypted_msg  = ''.join(x for x in msgBit8Int)

    print('Decrypted Message')
    print(decrypted_msg)
    return

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
