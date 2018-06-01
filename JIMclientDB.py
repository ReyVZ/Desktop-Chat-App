from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///Client.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class History(Base):
    __tablename__ = 'History'
    msgId = Column(Integer, primary_key=True)
    contact = Column(String)
    message = Column(String)

    def __init__(self, contact, message):
        self.contact = contact
        self.message = message


Base.metadata.create_all(engine)


class JIMclientDB:
    def __init__(self, filename='sqlite:///Client.db'):
        self.engine = create_engine(filename)
        self.Session = sessionmaker(bind=engine)
        self.session = Session()

    def log(self, receiver, message):
        new_log = History(receiver, message)
        self.session.add(new_log)
        self.session.commit()

