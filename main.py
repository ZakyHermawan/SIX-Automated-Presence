# from presence import presence
from six_presence.presence_by_request import presence
import json
import os

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path,'credentials.json'), 'r') as f:
    credentials = json.load(f)

# def success(classcode, message):
#     print(f"Successful presence for {classcode} class")


# def fail(code, classcode, message):
#     print(f"Fail {code}. Reason: {message}")

def success():
    print('yey')

def fail(status):
    print(f'no >:( {status}')

presence(credentials['username'], credentials['password'], success_callback=success, fail_callback=fail)
