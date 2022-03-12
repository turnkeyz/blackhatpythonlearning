import socket

#declaring localhost and port number
host = '127.0.0.1'
port = 9997

#declaring our socket as udp type connection
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#sending some data
client.sendto(b"SENDING DATA",(host,port))

#receiving data
data, addr = client.recvfrom(16024)

#print and close connection
print(data.decode())
client.close()