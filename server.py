from socket import *
import time
import sys
import argparse
import json
import select
import logging
import log_config
from JIMserver import JIMserver


log = logging.getLogger('app')


def log_decorator(func):
    def call(*args, **kwargs):
        log_args = args
        log_kwargs = kwargs
        return func(*args, **kwargs)
    call.__name__ = func.__name__
    call.__dict__.update(func.__dict__)
    return call


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=7777)
    parser.add_argument('-a', default='')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    server = JIMserver('', int(namespace.p))
    clients = []

    while True:
        try:
            client, addr = server.s.accept()
        except:
            pass
        else:
            clients.append(client)
            print('Connected with: {}'.format(str(addr)))
            log.info('Connected with: {}'.format(str(addr)))
            server.db.mark(time.ctime(), str(addr))
        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass
            for client in r:
                try:
                    data = server.read(client)
                    reply = server.create_reply(data)
                except:
                    print('Disconnected with: {}'.format(client.getsockname()))
                    log.info('Disconnected with: {}'.format(client.getsockname()))
                    client.close()
                    clients.remove(client)
                for client in w:
                    try:
                        server.send(client, reply)
                    except:
                        pass
 
