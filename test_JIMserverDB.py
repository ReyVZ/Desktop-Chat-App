import pytest
from JIMserverDB import JIMserverDB, Client, History, Contacts


@pytest.fixture
def db():
    filename = 'sqlite:///Server.db'
    db = JIMserverDB(filename)
    return db

def test_auth(db):
    db.auth('test_user', 'password')
    res = db.session.query(Client).filter(Client.login=='test_user').all()
    assert res[0].password == 'password'

def test_mark(db):
    db.mark('Fri Dec 22 20:52:34 2017', "('127.0.0.1', 43136)")
    res = db.session.query(History).filter(History.time=='Fri Dec 22 20:52:34 2017').all()
    assert res[0].ip == "('127.0.0.1', 43136)"

def test_contacts(db):
    db.contacts('test_user', 'test_contact')
    res = db.session.query(Contacts).filter(Contacts.owner=='test_user').all()
    assert res[len(res)-1].contact == 'test_contact'

def test_get_contacts(db):
    res = db.get_contacts('test_user')
    assert res[0] == 'test_contact'
