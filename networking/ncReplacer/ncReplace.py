#this is for educational purposes only and should not be used for any other purpose.
#this is following and putting my on take on Black Hat Python basic concepts 
#from what I have learned and am studying.

import socket
import argparse
import subprocess
import sys
import shlex
import textwrap
import threading
import NetCat

#we are basically writing up a function that will take any command we submit run it 
#(via the subprocess library) and then output the results of the command
#if there is an error it returns the error from the shell response.
def execute(commandGoesHere):
    commandGoesHere = commandGoesHere.strip()
    if not commandGoesHere:
        pass
    output = subprocess.check_output(shlex.split(commandGoesHere),
                                        stderr=subprocess.STDOUT)

    return output.decode()

class NetCat:
    def __init__(self,args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,
        socket.SO_REUSEADDR,1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()


    def send(self):
        self.socket.connect((self.args.target,self.args.port))

        if self.buffer:
            self.socket.send(self.buffer)
        
        try:
            while True:
                recv_len =1 
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response+=data.decode()
                    if recv_len<4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('user terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self,client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'ncReplace: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(4096)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.decode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server died{e}')
                    self.socket.close()
                    sys.exit()

#now onto building the parser
if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='replace the nc command tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            ncReplace.py -t 127.0.0.1 -p 8080 -l -c
            ncReplace.py -t 127.0.0.1 -p 8080 -l -u=mytest.txt
            ncReplace.py -t 127.0.0.1 -p 8080 -l -e=\"cat /etc/passwd\"
            echo 'this is test' | ./ncReplace.py -t 127.0.0.1 -p 3333
            ncReplace.py -t 127.0.0.1 -p 8080
            '''))
    parse.add_argument('-c', '--command', action='store_true', help='this is cmd')
    parse.add_argument('-u', '--upload', help='this is file upload command')
    parse.add_argument('-e', '--execute', help='this executes our command')
    parse.add_argument('-t', '--target', help='this configures our target')
    parse.add_argument('-l', '--listen', action='store_true',help='this listens')
    parse.add_argument('-p', '--port', type=int, default=3333, help='this configures our port')
    args = parse.parse_args()
    
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode())
    nc.run()
