import random
import os
import time

import cx_Oracle
import Encryption as ENC

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
conn = cx_Oracle.connect(user=r'STUDENT', password='STUDENT', dsn=dsn_tns)
c = conn.cursor()
add_counter = 0
c.execute('select * from filedatabase')
for row in c:
    print(row)
    add_counter = add_counter + 1

print(add_counter)


def add(params):
    print(params)
    global add_counter
    dsn_tns_enc = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
    conn_enc = cx_Oracle.connect(user=r'STUDENT', password='STUDENT', dsn=dsn_tns_enc)
    p = ENC.generate_large_prime()
    q = ENC.generate_large_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, 2 ** 32)
    # phi and e must be coprime and e < phi
    while True:
        if ENC.gcd(phi, e) == 1 and e < phi:
            break
        e = random.randint(2, 2 ** 32)

    d = ENC.modular_multiplicative_inverse(e, phi)
    if os.path.exists(params[1]):
        file = open(params[1], "r")
        plain_text = file.read()
        file.close()
        int_plain_text = int.from_bytes(plain_text.encode(), byteorder='little')
        encrypted_text = pow(int_plain_text, e, n)
        encrypted_file = open("EncryptedFiles\\file" + str(add_counter), "w")
        add_counter = add_counter + 1
        encrypted_file.write(str(encrypted_text))

    else:
        print("The file you specified is not in the current directory! Please move it into the current directory "
              "and try again")
        return

    name, extension = os.path.splitext(params[1])
    c_enc = conn_enc.cursor()
    sql = """insert into filedatabase 
          values (:f_id, :f_name, :f_type, :f_size, :f_changed, :f_modified, :f_accessed, :f_public_key)"""
    c_enc.execute(sql, [add_counter, name, extension, os.path.getsize(params[1]),
                        str(time.ctime(os.path.getctime(params[1]))), str(time.ctime(os.path.getmtime(params[1]))),
                        str(time.ctime(os.path.getatime(params[1]))), str(e)])
    conn_enc.commit()
    os.remove(params[1])


def show(params):
    print(params)


def remove(params):
    print(params)


def handle_command(params):
    handler = {
        "add": add,
        "show": show,
        "remove": remove
    }
    return handler[params[0]](params)


print("Welcome to Encrypted Database Tool! Type help for getting the instructions about the commands!")
while 1:
    print("----------")
    command = input('Enter a command: ')
    if command.lower() == "exit":
        break
    if command.lower() == "help":
        f = open("instructions.txt")
        print("----------")
        print(f.read())
    else:
        command = command.split(" ")
        if command[0] != "add" and command[0] != "show" and command[0] != "remove":
            print("Wrong command! Type help to see the commands!")
            continue
        if command[0] == "show" and len(command) != 4:
            print("Wrong syntax of show command! Type help to see the commands!")
            continue
        if (command[0] == "add" or command[0] == "remove") and len(command) != 2:
            if command[0] == "add":
                print("Wrong syntax of add command! Type help to see the commands!")
                continue
            if command[0] == "remove":
                print("Wrong syntax of remove command! Type help to see the commands!")
                continue

        handle_command(command)
