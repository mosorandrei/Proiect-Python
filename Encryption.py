import rsa

publicKey, privateKey = rsa.newkeys(512)

f = open("test.txt", "rb")
message = f.read()

encMessage = rsa.encrypt(str(message).encode(),
                         publicKey)

print("original string: ", message)
print("encrypted string: ", encMessage)

enc_f = open("encrypted_file.txt", "wb")
enc_f.write(encMessage)

decMessage = rsa.decrypt(encMessage, privateKey).decode()

print("decrypted string: ", decMessage)