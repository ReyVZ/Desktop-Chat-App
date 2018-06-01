import hashlib
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///Server.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Client(Base):
    __tablename__ = 'Client'
    userId = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    def __init__(self, login, password):
        self.login = login
        self.password = password


class History(Base):
    __tablename__ = 'History'
    logId = Column(Integer, primary_key=True)
    time = Column(String)
    ip = Column(String)

    def __init__(self, time, ip):
        self.time = time
        self.ip = ip


class Contacts(Base):
    __tablename__ = 'Contacts'
    contactId = Column(Integer, primary_key=True)
    owner = Column(String)
    contact = Column(String)

    def __init__(self, owner, contact):
        self.owner = owner
        self.contact = contact


Base.metadata.create_all(engine)


class JIMserverDB:
    def __init__(self, filename='sqlite:///Server.db'):
        self.engine = create_engine(filename)
        self.Session = sessionmaker(bind=engine)
        self.session = Session()

    def auth(self, login, password):
        user = Client(login, password)
        self.session.add(user)
        self.session.commit()

    def mark(self, time, ip):
        log = History(time, ip)
        self.session.add(log)
        self.session.commit()

    def contacts(self, owner, contact):
        contact = Contacts(owner, contact)
        self.session.add(contact)
        self.session.commit()

    def get_contacts(self, user):
        users = self.session.query(Contacts).filter(Contacts.owner==user).all()
        lst = []
        for u in users:
            lst.append(u.contact)
        return lst

    def authentication(self, login, password):
        salt = 'Abbro Cadabbro'
        try:
            user = self.session.query(Client).filter(Client.login==login).one()
        except:
            return False
        else:
            dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            print(dk)
            print(user.password)
            if user and user.password == dk:
                return True
            else:
                return False

if __name__ == '__main__':
    db = JIMserverDB()
    import hashlib

    salt = 'Abbro Cadabbro'
    login = input("Enter new user's login: ")
    while True:
        password = input("Enter new user's password: ")
        password_repeat = input("Enter new user's password once more: ")
        if password == password_repeat:
            break
        else:
            print('Try once more!')
            continue

    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    db.auth(login, dk)
