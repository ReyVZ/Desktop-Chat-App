import time
import json


class JIMmsg:
    def auth_msg(self, account_name, password):
        msg = {
            'action': 'authenticate',
            'time': time.ctime(),
            'user': {
                'account_name': account_name,
                'password': password
            }
        }
        return json.dumps(msg)

    def pres_msg(self, account_name, status):
        msg = {
            'action': 'presence',
            'time': time.ctime(),
            'user': {
                'account_name': account_name,
                'status': status
            }
        }
        return json.dumps(msg)

    def from_to_msg(self, sender, receiver, message):
        msg = {
            'action': 'msg',
            'time': time.ctime(),
            'to': receiver,
            'from': sender,
            'message': message
        }
        return json.dumps(msg)

    def join_msg(self, room_name):
        msg = {
            'action': 'join',
            'time': time.ctime(),
            'room': room_name
        }
        return json.dumps(msg)

    def leave_msg(self, room_name):
        msg = {
            'action': 'leave',
            'time': time.ctime(),
            'room': room_name
        }
        return json.dumps(msg)

    def quit_msg(self):
        msg = {
            'action': 'quit'
        }
        return json.dumps(msg)

    def get_contacts_msg(self, account_name):
        msg = {
            'action': 'get_contacts',
            'account_name': account_name,
            'time': time.ctime()
        }
        return json.dumps(msg)






