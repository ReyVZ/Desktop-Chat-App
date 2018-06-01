import json
from socket import *
from JIMresponse import JIMresponse
from JIMmsg import JIMmsg
from JIMserverDB import JIMserverDB
import logging
import log_config


log = logging.getLogger('app')


class JIMserver:
    def __init__(self, host, port):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(5)
        self.s.settimeout(0.2)
        log.info('SERVER UP. HOST: {} - PORT: {}'.format(host, port))
        self.db = JIMserverDB()
        log.info('DB UP.')

    def read(self, client):
        msg = client.recv(1024)
        data = json.loads(msg.decode('ascii'))
        log.info('INCOMING MSG:\n\t{}'.format(data))
        return data

    def send(self, client, msg):
        log.info('OUTGOING MSG:\n\t{}'.format(msg))
        client.send(msg.encode('ascii'))

    def create_reply(self, data):
        if data['action'] == 'presence':
            reply = JIMresponse()
            return reply.confirm_response(200, 'Hello {}'.format(data['user']['account_name']))

        if data['action'] == 'msg':
            reply = JIMmsg()
            self.db.contacts(data['from'], data['to'])
            return reply.from_to_msg(data['from'], data['to'], data['message'])

        if data['action'] == 'get_contacts':
            users = self.db.get_contacts(data['account_name'])
            reply = JIMresponse()
            return reply.send_contacts(users)

        if data['action'] == 'authenticate':
            login = data['user']['account_name']
            password = data['user']['password']
            reply = JIMresponse()
            result = self.db.authentication(login, password)
            if result is True:
                return reply.confirm_response(202, 'Authentication is OK')
            if result is False:
                return reply.confirm_response(402, 'Authentication is failed')
