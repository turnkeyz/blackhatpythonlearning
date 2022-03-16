#this is for educational purposes only and should not be used for any other purpose.
#this is following and putting my on take on Black Hat Python basic concepts 
#from what I have learned and am studying.
import socket

#establish our variables for who we want to test against
target = "www.google.com"
port = 80

#setting up socket object named "client"
##AF_INET specifies standard ipv4 connection
##SOCK_STREAM specifies it will be a tcp connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connection to client via variables
client.connect((target,port))

#sending data to our client via http get request"
client.send(b'get / HTTP/1.1\r\nHost: google.com\r\n\r\n')

#specify response size
response = client.recv(16240)

#print response
print(response.decode())
client.close()