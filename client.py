from socket import *
import sys
import time
import json
from PyQt5.QtWidgets import QApplication
from JIMclient import JIMclient


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = JIMclient('localhost', 7777)
    client.show()
    sys.exit(app.exec_())
