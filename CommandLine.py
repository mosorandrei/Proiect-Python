import math
import random
import os
import time
import cx_Oracle
import Encryption as Enc

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
conn = cx_Oracle.connect(user=r'STUDENT', password='STUDENT', dsn=dsn_tns)
c = conn.cursor()
add_counter = 0
c.execute('select * from filedatabase')

for row in c:
    print(row)


def add(params):
    global add_counter, dsn_tns, conn

    p = Enc.generate_large_prime()
    q = Enc.generate_large_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, 2 ** 32)
    # phi and e must be coprime and e < phi
    while True:
        if Enc.gcd(phi, e) == 1 and e < phi:
            break
        e = random.randint(2, 2 ** 32)

    d = Enc.modular_multiplicative_inverse(e, phi)
    # here we print the private key only for testing purposes
    print(d)
    ciphertext = ""
    if os.path.exists(params[1]):
        file = open(params[1], "r")
        plain_text = file.read()
        file.close()
        if len(plain_text) % 4 != 0:
            for i in range(4 - (len(plain_text) % 4)):
                plain_text = plain_text + " "

        for i in range(0, len(plain_text), 4):
            part = plain_text[i:i + 4]
            int_plain_text = int.from_bytes(part.encode(), byteorder='little')
            encrypted_text = pow(int_plain_text, e, n)
            ciphertext = ciphertext + str(encrypted_text) + "\n"

        add_counter = random.randint(0, 1000)
        cr = conn.cursor()
        cr.execute('select * from filedatabase')
        ok = 1
        while ok == 1:
            ok = 0
            for r in cr:
                if r[0] == add_counter:
                    add_counter = random.randint(0, 1000)
                    ok = 1
        encrypted_file = open("EncryptedFiles\\file" + str(add_counter) + ".txt", "w")
        encrypted_file.write(ciphertext)
        encrypted_file.close()

    else:
        print("The file you specified is not in the current directory! Please move it into the current directory "
              "and try again")
        return

    name, extension = os.path.splitext(params[1])
    c_enc = conn.cursor()
    sql = """insert into filedatabase 
          values (:f_id, :f_name, :f_type, :f_size, :f_changed, :f_modified, :f_accessed, :f_public_key, 
          :f_product_prime)"""
    c_enc.execute(sql, [add_counter, name, extension, os.path.getsize(params[1]),
                        str(time.ctime(os.path.getctime(params[1]))), str(time.ctime(os.path.getmtime(params[1]))),
                        str(time.ctime(os.path.getatime(params[1]))), str(e), str(n)])
    conn.commit()
    os.remove(params[1])


def show(params):
    global dsn_tns, conn
    print("###")
    print("Careful! In order to decrypt your file properly you must provide the right secret key,"
          "otherwise, you will get a wrong output! ")
    print("###")
    d = int(input("----Enter the secret key: "))

    file_name = params[-1].split(".")[0]
    file_id = ""
    c_dec = conn.cursor()
    sql = "select * from filedatabase where file_name = :f_name"
    c_dec.execute(sql, f_name=file_name)
    n = 0
    rows_list = []
    for rand in c_dec:
        file_id = rand[0]
        n = int(rand[-1])
        rows_list.append((rand, n, file_id))

    if len(rows_list) == 0:
        print("The name of the file you requested is not in our database! Please check again the name and try again!")
        return

    if len(rows_list) > 1:
        file_id = int(input("There are multiple files in the database with the name you provided! "
                            "Please provide the id of your file: "))

    ok = 0
    for r in rows_list:
        if r[2] == file_id:
            ok = 1
            print("########################")
            rand = r[0]
            n = int(rand[-1])
            print("The information about your file is:")
            print("The id of the file is : " + str(rand[0]))
            print("The original name of the file is: " + str(rand[1]))
            print("The extension of the file is: " + str(rand[2]))
            print("The size of the file is: " + str(rand[3]))
            print("The creation date is: " + str(rand[4]))
            print("The last modification date is: " + str(rand[5]))
            print("The last access date is: " + str(rand[6]))
            print("The public key is: " + str(rand[7]))
            print("########################")
            break

    if ok == 0:
        print("###")
        print("The id you provided is not in our database! Please try again!")
        print("###")
        return

    plaint_text = ""
    encrypted_file = open("EncryptedFiles\\file" + str(file_id) + ".txt", "r")
    encrypted_text = encrypted_file.read()
    encrypted_text = encrypted_text.split("\n")
    for i in range(len(encrypted_text) - 1):
        content = pow(int(encrypted_text[i]), d, n)
        length = math.ceil(content.bit_length() / 8)
        plaint_text = plaint_text + content.to_bytes(length, byteorder="little").decode()

    print("The content of the selected file is:")
    print("%%%%%%%%%%%%%%%%%%")
    print(plaint_text)
    print("%%%%%%%%%%%%%%%%%%")


def remove(params):
    global dsn_tns, conn
    file_name = params[-1].split(".")[0]
    file_id = ""
    c_rem = conn.cursor()
    sql = "select * from filedatabase where file_name = :f_name"
    c_rem.execute(sql, f_name=file_name)
    rows_list = []
    for rand in c_rem:
        file_id = rand[0]
        rows_list.append(file_id)
    if len(rows_list) == 0:
        print("The name of the file you requested to delete is not in our database!"
              " Please check again the name and try again!")
        return

    if len(rows_list) > 1:
        file_id = int(input("There are multiple files in the database with the name you provided! "
                            "Please provide the id of your file you want to delete"
                            ": "))

    cd = conn.cursor()
    cd.execute('select * from filedatabase')
    ok = 0
    for r in cd:
        if r[0] == file_id:
            ok = 1
            break

    if ok == 0:
        print("###")
        print("The id you provided is not in our database! Please try again!")
        print("###")
        return

    c_rem = conn.cursor()
    sql = "delete from filedatabase where file_name = :f_name and file_id = :f_id"
    c_rem.execute(sql, f_name=file_name, f_id=file_id)
    conn.commit()
    os.remove("EncryptedFiles\\file" + str(file_id) + ".txt")

    print("The file " + str(params[1]) + " was deleted successfully")


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
