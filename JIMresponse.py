import time
import json


class JIMresponse:
    def info_response(self, code, alert):
        response = {
            'response': code,
            'time': time.ctime(),
            'alert': alert
        }
        return json.dumps(response)

    def confirm_response(self, code, alert):
        response = {
            'response': code,
            'time': time.ctime(),
            'alert': alert
        }
        return json.dumps(response)

    def client_error_response(self, code, error):
        response = {
            'response': code,
            'time': time.ctime(),
            'error': error
        }
        return json.dumps(response)

    def server_error_response(self, code, error):
        response = {
            'response': code,
            'time': time.ctime(),
            'error': error
        }
        return json.dumps(response)

    def probe_response(self):
        response = {
            'action': 'probe',
            'time': time.ctime()
        }
        return json.dumps(response)

    def send_quantity_contacts(self, quantity):
        response = {
            'response': 202,
            'quantity': quantity
        }
        return json.dumps(response)

    def send_contacts(self, users):
        response = {
            'action': 'contact_list',
            'users': users
        }
        return json.dumps(response)

