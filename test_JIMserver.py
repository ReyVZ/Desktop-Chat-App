from socket import *
import pytest
import json
import random
from JIMserver import JIMserver


@pytest.fixture
def con(request):
    port = random.randint(7777, 8000) 
    server = JIMserver('', port)

    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('localhost', port))

    con, addr = server.s.accept()
    def con_teardown():
        client.close()
        con.close()
        server.s.close()
    request.addfinalizer(con_teardown)
    return con, client, server


def test_read(con):
    con[1].send('Hello'.encode('ascii'))
    data = con[0].recv(1024)
    msg = data.decode('ascii')
    assert msg == 'Hello'          


def test_create_reply(con):
    msg = {
        'action': 'get_contacts',
        'account_name': 'test_user',
        'time': 'not matter'
    }
    expected = {'test_contact'}
    lst = con[2].create_reply(msg) 
    lst = json.loads(lst)
    contact = set(lst['users'])
    assert contact == expected

def test_send(con):
    msg = 'test_Hello'
    con[2].send(con[0], msg)
    data = con[1].recv(1024)
    assert data.decode('ascii') == msg
    
    
    






    
