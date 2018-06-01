import pytest
from JIMclientDB import JIMclientDB, History


@pytest.fixture
def db():
    filename = 'sqlite:///Client.db'
    db = JIMclientDB(filename)
    return db

def test_log(db):
    db.log('test_contact', 'Hello')
    res = db.session.query(History).filter(History.contact=='test_contact').all()
    assert res[len(res)-1].message == 'Hello'

