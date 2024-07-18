import socket
import AES_simulation as aes
import diffie_hellman as dh

aes_len = 128

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

client.connect(('127.0.0.1', port))

# receive data from the server
msg = client.recv(1024).decode()
print(msg)
[p, g, A] = msg.split(",")

p = int(p)
g = int(g)
A = int(A)

b = dh.generate_b(aes_len)
B = dh.generate_B(g, b, p)

client.send(str(B).encode())

key = dh.get_s(A, b, p)
print('Key: ', key)
key_bin = bin(key)[2:]
print('Key in binary: ', key_bin)

encrypted_text = client.recv(1024).decode()
print('Encrypted text: ', encrypted_text)
decripted_text = aes.decrypt(encrypted_text, key_bin)
print('Decrypted text: ', aes.convert_to_string(decripted_text))

# close the connection
client.close()