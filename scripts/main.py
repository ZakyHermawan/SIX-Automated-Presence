from six_presence.presence import fill_presence
import json
import os

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path,'credentials.json'), 'r') as f:
    credentials = json.load(f)

def success():
    print('Presence success, callback lies here')

def fail(status):
    print(f'Presence unsuccessful with status {status}, callback lies here')

fill_presence(credentials['username'], credentials['password'], success_callback=success, fail_callback=fail)
