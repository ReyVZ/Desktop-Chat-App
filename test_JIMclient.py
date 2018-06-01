from socket import *
import pytest
import random
import json
from JIMclient import JIMclient


@pytest.fixture 
def cons(request): 
    port = random.randint(7777, 8000)  
    ser = socket(AF_INET, SOCK_STREAM) 
    ser.bind(('', port))
    ser.listen(5)

    cl = JIMclient('localhost', port, 'test_user')
 
    client, addr = ser.accept() 
    
    def client_teardown(): 
        client.close() 
        cl.s.close() 
        ser.close() 
    request.addfinalizer(client_teardown) 
    return cl, client, ser


def test_read(cons):
    data = {'action': 'contact_list', 'users': ['test_contact']}
    data = json.dumps(data)
    cons[1].send(data.encode('ascii'))
    assert cons[0].read() == True

def test_write(cons):
    cons[0].msg = 'test_Hello'
    cons[0].write()
    data = cons[1].recv(1024)
    assert data.decode('ascii') == 'test_Hello'

def test_create_msg(cons):
    print('You need to enter: "hello" and "test_contact"')
    cons[0].create_msg()
    data = json.loads(cons[0].msg)
    msg = data['message']
    contact = data['to']
    assert msg == 'hello' and contact == 'test_contact' 

def test_get_contacts(cons):
    cons[0].get_contacts()
    data = json.loads(cons[0].msg)
    user = data['account_name']
    assert user == 'test_user'
















    
    



