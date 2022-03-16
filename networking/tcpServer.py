#this is for educational purposes only and should not be used for any other purpose.
#this is following and putting my on take on Black Hat Python basic concepts 
#from what I have learned and am studying.
#this will be my first ever tcp server
from http import client
from ipaddress import ip_address
import socket
import threading
import os
from dotenv import load_dotenv

load_dotenv()

#modified original example to include env variables that may be useful
#in the event that you have some data you don't want shown or 
#uploaded to github
#if our env variable doesn't return a valid response it defaults
#to localhost
ip_address = os.getenv('url')
#implemented for port as well
PORT = 8080

def main():
    #create our server object with the socket network layer interface
    tcp_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #binds ip and port to our server object
    tcp_serv.bind((ip_address,PORT))
    #createt amount of connections possible that wil be logged
    tcp_serv.listen(10)
    #print(f'[*] Listening on {ip_address}:{PORT}')

    #keep process running unless manually quit
    while 1==1:
        #create the process of our server accepting incoming 
        #requests
        client, address = tcp_serv.accept()
        print(f'[*] Connection accepted from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()
def handle_client(client_sock):
    #defining the handle process and allocating a size of 
    #data to receive and log request as utf-8
    request = client_sock.recv(4096)
    print(f'[*] Received: {request.decode("utf-8")}')
    client_sock.send(b'ACK')

if __name__ == '__main__':
    main()
 