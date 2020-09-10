from presence import presence
import json

with open('credentials.json', 'r') as f:
  credentials = json.load(f)

def success():
  print('yey')

presence(credentials['username'], credentials['password'], success, headless=False)