# -*- coding: utf-8 -*-

from itertools import islice
from random import randint
import base64


class Rsa:
    def __init__(self, message, key_open=None, key_close=None):
        self.message = message
        self.key_open = key_open
        self.key_close = key_close

    def generate_enc_message(self):

        # ГЕНЕРАЦИЯ ПРОСТЫХ ЧИСЕЛ В СПИСОК
        def primes():
            if hasattr(primes, "D"):
                D = primes.D
            else:
                primes.D = D = {}

            def sieve():
                q = 2
                while True:
                    if q not in D:
                        yield q
                        D[q * q] = [q]
                    else:
                        for p in D[q]:
                            D.setdefault(p + q, []).append(p)
                        del D[q]
                    q += 1

            return sieve()

        n = (list(islice(primes(), 1, 45)))

        # ВЫБОР ДВУХ ПРОСТЫХ ЧИСЕЛ
        a = n[randint(1, len(n))]
        b = n[randint(1, len(n))]
        N = a * b

        # ФУНКЦИЯ ЭЙЛЕРА
        def func_f(a, b):
            return (a - 1) * (b - 1)

        func_eiler = func_f(a, b)

        # ОТКРЫТАЯ ЭКСПОНЕНТА

        def ecspon_open(t):
            for i in range(2, 100):
                f = t / i
                if int(f) != float(f):
                    return i

        e = ecspon_open(func_eiler)

        # СЕКРЕТНАЯ ЭКСПОНЕНТА

        def ecspon_sicrit(func_eiler, e):
            for i in range(3, 100):
                d = (func_eiler * i + 1) / e
                if int(d) == float(d):
                    d = int(d)
                    return d

        r = ecspon_sicrit(func_eiler=func_eiler, e=e)

        # ПРЕОБРАЗОВАНИЕ БУКВ В ЧИСЛА С ПОМОЩЬЮ ORD
        word = self.message
        list_word_index = [ord(i) for i in word]

        # ШИФРОВАНИЕ СПИСКА(СООБЩЕНИЯ)
        encript_msg = []

        def encript_massage(list1, e, N):
            for i in range(len(list1)):
                q = (list1[i] ** e) % N
                encript_msg.append(q)
            return encript_msg

        # ИЗ СПИСКА ЦИФР В base64
        encript = encript_massage(list_word_index, e, N)
        wordList = [num.to_bytes(2, byteorder='big') for num in encript]
        encoded = b''.join(wordList)

        # ПОМЕЩЕНИЕ ОТКРЫТОЙ ЭКСПОНЕНТЫ И СУММЫ В СПИСОК e = открытая эксп r.txt = секретная эксп N = сумма

        def open_key(e, N):
            list_key = [N, e]
            return list_key

        key_enc = open_key(e, N)
        key_dec = open_key(r, N)

        # СПИСОК ИЗ СЕКРЕТНОЙ ЭКСП ИЛИ ОТКРЫТОЙ И СУММЫ в base64
        def base64_key(key):
            wordList = [num.to_bytes(2, byteorder='big') for num in key]
            encoded = b''.join(wordList)
            return base64.b64encode(encoded).decode('ascii')

        return [(key_enc, key_dec, encript),
                (base64_key(key_enc), base64_key(key_dec), base64.b64encode(encoded).decode('ascii'))]

    def encript(self, key, message):
        word = message
        list_word_index = [ord(i) for i in word]
        byte_key = base64.b64decode(key)
        decr_key = [int.from_bytes(byte_key[i:i + 2], byteorder='big') for i in range(0, len(byte_key), 2)]

        # ШИФРОВАНИЕ СПИСКА(СООБЩЕНИЯ)
        encript_msg = []

        def encript_massage(list1, e, N):
            for i in range(len(list1)):
                q = (list1[i] ** e) % N
                encript_msg.append(q)
            return encript_msg

        # ИЗ СПИСКА ЦИФР В base64
        encript = encript_massage(list_word_index, decr_key[-1], decr_key[0])
        wordList = [num.to_bytes(2, byteorder='big') for num in encript]
        encoded = b''.join(wordList)

        return base64.b64encode(encoded).decode('ascii')

    def decript(self, key, message):

        def decript_massage(encript_msg):
            byte_str = base64.b64decode(encript_msg)
            return [int.from_bytes(byte_str[i:i + 2], byteorder='big') for i in range(0, len(byte_str), 2)]

        # КЛЮЧ ИЗ base64 В СПИСОК ЦИФР

        byte_key = base64.b64decode(key)
        decr_key = [int.from_bytes(byte_key[i:i + 2], byteorder='big') for i in range(0, len(byte_key), 2)]

        f = []

        def decript(enc, decr_key, f):
            for i in range(len(enc)):
                b = enc[i] ** decr_key[1]
                resalt = b % decr_key[0]
                f.append(resalt)
            return f

        resalt_decript = decript(decript_massage(message), decr_key, f)
        final_result = [chr(i) for i in resalt_decript]
        return ''.join(final_result)



# ('He8ABQ==', 'He8RjQ==', 'ENIICgMNDBkMZAgKAw0XZx1oCAo=')]