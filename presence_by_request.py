import requests
import json
import time
from bs4 import BeautifulSoup

login_url = 'https://login.itb.ac.id/cas/login?service=https://akademik.itb.ac.id/login/INA'

# Load credentials
with open('credentials.json') as f:
    credentials = json.load(f)

# Create session for persisting cookies throughout requests
with requests.Session() as session:
    session = requests.Session()

# Load login page
login_page_request = session.get(login_url)

# Get token from loading page
login_page_token = BeautifulSoup(login_page_request.text, 'html.parser').find_all('input')[2]['value']

# POST login data
login_data = {
    "username": credentials['username'],
    "password": credentials['password'],
    "execution": login_page_token,
    "_eventId": "submit",
    "geolocation": ""
}
six_page_html = session.post(login_url, login_data).text

# Find class link
class_link = list(map(lambda div: div.find('a'), BeautifulSoup(six_page_html, 'html.parser').findAll('div',{"class": "col-xs-4 col-sm-3 col-md-2 text-center"})))[3]

# GET request for getting the links of the classes today
class_page_html = session.get(f'https://akademik.itb.ac.id{class_link["href"].strip()}').text
classes_links = BeautifulSoup(class_page_html, 'html.parser').find('td', {"class": "bg-info"}).find_all('a')
classes_today = list(map(lambda c: {"name": c['data-kuliah'], "start_time": c.text.strip()[:5], "end_time": c.text.strip()[6:11], "url": c['data-url']}, classes_links))

# Get current server time (GMT +7)
t = time.gmtime(time.time() + 25200)
current_time = time.strftime("%H:%M", t)

# Try to fill presence form for each link
for c in classes_today:
  try:
    class_html = BeautifulSoup(session.get(f'https://akademik.itb.ac.id{c["url"]}').text, 'html.parser')
    class_action = class_html.find('form')['action']
    class_token = class_html.find_all('input')[1]['value']
    
    # Check if presence form is filled
    if(class_html.find('button', {"name": "form[tidakhadir]"}) is not None):
        raise Exception()

    presence_data = {
        "form[hadir]": "",
        "form[returnTo]": class_link["href"].strip(),
        "form[_token]": class_token,
    }

    result = session.post(f'https://akademik.itb.ac.id{class_action}', presence_data)
    print(f'Presence successfully filled for {c["name"]}')
  except:
    print(f'Can\'t fill presence for {c["name"]}')

  