from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('filekey.key', 'wb') as fk:
    fk.write(key)

with open('filekey.key', 'rb') as fk:
    key = fk.read()

fernet = Fernet(key)

with open('TestFile.txt', 'rb') as f:
    original = f.read()

print(original)

encrypted = fernet.encrypt(original)

with open('TestFile.txt', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

print(encrypted)

fernet = Fernet(key)

with open('TestFile.txt', 'rb') as enc_file:
    encrypted = enc_file.read()

decrypted = fernet.decrypt(encrypted)

with open('TestFile.txt', 'wb') as dec_file:
    dec_file.write(decrypted)

print(decrypted)
