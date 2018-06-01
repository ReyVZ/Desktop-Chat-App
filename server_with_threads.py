from socket import *
from threading import Thread, Lock
import json
from JIMresponse import JIMresponse
from JIMmsg import JIMmsg

DATA = {}

class Receiver:
    def __init__(self, sock):
        self.s = sock
    
    def __call__(self):
        while True:
            data = self.s.recv(1024).decode('ascii')
            if data:
                data = json.loads(data)
                print(data, '\n')
                if data['action']:
                    global DATA
                    DATA = data
                    print(DATA)


class Sender:
    def __init__(self, sock):
        self.s = sock
    
    def __call__(self):
        while True:
            try:
                global DATA
                if DATA['action'] == 'presence':
                    reply = JIMresponse()
                    data = reply.confirm_response(200, 'Hello {}'.format(DATA['user']['account_name']))
                    self.s.send(data.encode('ascii'))
                    DATA = {}

                if DATA['action'] == 'msg':
                    reply = JIMmsg()
                    data = reply.from_to_msg(DATA['from'], DATA['to'], DATA['message'])
                    self.s.send(data.encode('ascii'))
                    DATA = {}

                if DATA['action'] == 'get_contacts':
                    users = ['Mom', 'Dad', 'Bro']
                    reply = JIMresponse()
                    data = reply.send_contacts(users)
                    self.s.send(data.encode('ascii'))
                    DATA = {}
            except:
                pass


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(5)
        while True:
            client, addr = self.s.accept()

            receiver = Receiver(client)
            t_receiver = Thread(target=receiver)
            t_receiver.daemon = True

            sender = Sender(client)
            t_sender = Thread(target=sender)
            t_sender.daemon = True

            t_receiver.start()
            t_sender.start()


if __name__ == '__main__':
    server = Server('localhost', 7777)
    server.start()
