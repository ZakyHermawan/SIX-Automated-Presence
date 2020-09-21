from presence import presence
import json

with open('credentials.json', 'r') as f:
    credentials = json.load(f)

def success(classcode, message):
    print(f"Successful presence for {classcode} class")


def fail(code, classcode, message):
    print(f"Fail {code}. Reason: {message}")

presence(credentials['username'], credentials['password'], success_callback=success, fail_callback=fail, headless=False)
