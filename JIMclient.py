import json
from socket import *
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QInputDialog,
QMessageBox)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from JIMmsg import JIMmsg
from JIMclientDB import JIMclientDB

class Receiver(QObject):

    gotData = pyqtSignal(str)

    def __init__(self, s):
        super().__init__()
        self.s = s
    
    def read(self):
        while True:
            data = self.s.recv(1024).decode('ascii')
            if data:
                self.gotData.emit(data)
            else:
                break


class JIMclient(QWidget):
    def __init__(self, addr, port):
        super().__init__()
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((addr, port))
        self.user = ''
        self.password = ''
        self.opposite = 'test_contact'
        self.msg = ''
        self.full_chat = ''
        self.db = JIMclientDB()
        self.authentication()
        self.contacts = self.get_contacts()
        self.resize(400, 400)
        self.setWindowTitle("JIM Chat")
        self.initUI()

        self.receiver = Receiver(self.s)
        self.receiver.gotData.connect(self.update_chat)
        self.thread = QThread()
        self.receiver.moveToThread(self.thread)
        self.thread.started.connect(self.receiver.read)
        self.thread.start()
    
    def authentication(self):
        while True:
            dlg = QInputDialog()
            login, okPressed = dlg.getText(self, "LOGIN","Your login:", QLineEdit.Normal, "dre")
            if okPressed and login != '':
                self.user = login
            else:
                continue
            password, okPressed = dlg.getText(self, "PASSWORD","Your password:", QLineEdit.Normal, "12345")
            if okPressed and password != '':
                self.password = password
            else:
                continue
            m = JIMmsg()
            self.msg = m.auth_msg(self.user, self.password)
            self.s.send(self.msg.encode('ascii'))
            data = self.s.recv(1024)
            data = json.loads(data.decode('ascii'))
            if data['response'] == 202:
                break
            else:
                buttonReply = QMessageBox.question(self, data['alert'], "Try once more",
                QMessageBox.Yes, QMessageBox.Yes)
                if buttonReply == QMessageBox.Yes:
                    continue


    def initUI(self):
        pal = QPalette()
        pal.setBrush(QPalette.Window, QBrush(QPixmap('15gm.jpg')))
        self.setPalette(pal)

        self.switch = QLabel('Choose your contact:')
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.write)
        self.enter_area = QLineEdit()
        self.enter_area.setPlaceholderText('Your message:')
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.contact_list = QComboBox()
        self.contact_list.addItems(self.contacts)
        self.contact_list.activated[str].connect(self.onActivated)
        
        self.vboxl = QVBoxLayout()
        self.vboxl.addWidget(self.chat_area)
        self.vboxl.addWidget(self.enter_area)

        self.vboxr = QVBoxLayout()
        self.vboxr.addWidget(self.switch)
        self.vboxr.addWidget(self.contact_list)
        self.vboxr.addStretch(1)

        self.vboxr.addWidget(self.send_button)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vboxl)
        self.hbox.addLayout(self.vboxr)

        self.setLayout(self.hbox)

    @pyqtSlot(str)
    def update_chat(self, data):
        data = json.loads(data)
        msg = '{} -> {}: {}'.format(data['from'], data['to'], data['message'])
        self.full_chat = self.full_chat + msg + '\n'
        self.chat_area.setText(self.full_chat)   

    def write(self):
        self.create_msg()
        self.s.send(self.msg.encode('ascii'))

    def create_msg(self):
        text = self.enter_area.text()
        self.db.log(self.opposite, text)
        m = JIMmsg()
        self.msg = m.from_to_msg(self.user, self.opposite, text) 

    def get_contacts(self):
        m = JIMmsg()
        self.msg = m.get_contacts_msg(self.user)
        self.s.send(self.msg.encode('ascii'))
        data = self.s.recv(1024)
        data = json.loads(data.decode('ascii'))
        return list(set(data['users']))

    def onActivated(self, text):
        self.opposite = text
