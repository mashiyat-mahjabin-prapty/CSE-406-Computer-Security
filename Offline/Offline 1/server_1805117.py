# import socket library
import socket
import AES_simulation as aes
import diffie_hellman as dh

aes_len = 128
# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
server.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
server.listen(5)
print("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:
    
        # Establish connection with client.
        client, address = server.accept()
        print('Got connection from', address)

        p = dh.random_prime(aes_len)
        g = dh.primitive_root(p)
        a = dh.generate_a(aes_len)
        A = dh.generate_A(g, a, p)

        # convert p, g, A to a string
        msg = str(p) + ',' + str(g) + ',' + str(A)
        print(msg)
        # send p, g, A to the client
        client.send(msg.encode())
        
        msg = client.recv(1024).decode()
        B = int(msg)

        key = dh.get_s(B, a, p)
        print('Key: ', key)

        key_bin = bin(key)[2:]
        print('Key in binary: ', key_bin)

        plain_text = 'Two One Nine Two'
        encrypted_text = aes.encrypt(plain_text, key_bin)
        encrypted_text = aes.convert_to_string(encrypted_text)
        client.send(encrypted_text.encode())

        client.close()

        break

# close the connection
server.close()
