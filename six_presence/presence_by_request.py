import requests
import json
import time
import logging
from six_presence.status_code import RequestCode, RequestCodeMessage
from bs4 import BeautifulSoup

# Load credentials
def presence(username, password, fail_callback=lambda status: None, success_callback=lambda: None):

    # Set logging config
    logging.basicConfig(format='[%(asctime)s] - %(message)s', datefmt='%d %b %H:%M:%S', level=logging.INFO)

    # Create session for persisting cookies throughout requests
    logging.info('Creating session')
    session = requests.Session()

    # Load login page
    login_page_request = session.get('https://login.itb.ac.id/cas/login?service=https://akademik.itb.ac.id/login/INA')

    # Get token from loading page
    login_page_token = BeautifulSoup(login_page_request.text, 'html.parser').find_all('input')[2]['value']

    # POST login data, auto-redirected to SIX
    logging.info(f'Logging in for user {username}')
    login_data = {
        "username": username,
        "password": password,
        "execution": login_page_token,
        "_eventId": "submit",
        "geolocation": ""
    }
    six_page_html = session.post('https://login.itb.ac.id/cas/login?service=https://akademik.itb.ac.id/login/INA', login_data).text

    # Find class link
    # If not found, login is failed (status code INVALID_LOGIN)
    try:
        class_link = list(map(lambda div: div.find('a'), BeautifulSoup(six_page_html, 'html.parser').findAll('div',{"class": "col-xs-4 col-sm-3 col-md-2 text-center"})))[3]
        logging.info('Login succesful')
    except:
        logging.info(RequestCodeMessage.INVALID_LOGIN)
        fail_callback(RequestCode.INVALID_LOGIN)
        return (RequestCode.INVALID_LOGIN, RequestCodeMessage.INVALID_LOGIN, None)
    

    # GET request for getting the links of the classes today
    class_page_html = session.get(f'https://akademik.itb.ac.id{class_link["href"].strip()}').text
    classes_block = BeautifulSoup(class_page_html, 'html.parser').find('td', {"class": "bg-info"})

    # If nothing is highlighted, there's no class (status code NO_CLASS)
    if(classes_block is None):
        logging.info(RequestCodeMessage.NO_CLASS)
        fail_callback(RequestCode.NO_CLASS)
        return (RequestCode.NO_CLASS, RequestCodeMessage.NO_CLASS, None)

    classes_links = classes_block.find_all('a')
    classes_today = list(map(lambda c: {"name": c['data-kuliah'], "start_time": c.text.strip()[:5], "end_time": c.text.strip()[6:11], "url": c['data-url']}, classes_links))

    # Get current server time (GMT +7)
    t = time.gmtime(time.time() + 25200)
    current_time = time.strftime("%H:%M", t)

    # Try to fill presence form for each link
    for c in classes_today:
        if(c['start_time'] <= current_time <= c['end_time']):
            class_html = BeautifulSoup(session.get(f'https://akademik.itb.ac.id{c["url"]}').text, 'html.parser')
            
            # If presence form does not exist, presence failed (status code PRESENCE_NOT_OPEN)
            if(class_html.find('form') is None):
                logging.info(f'{RequestCodeMessage.INVALID_LOGIN} for {c["name"]}')
                fail_callback(RequestCode.PRESENCE_NOT_OPEN)
                return (RequestCode.PRESENCE_NOT_OPEN, RequestCodeMessage.PRESENCE_NOT_OPEN, c["name"])

            class_action = class_html.find('form')['action']
            class_token = class_html.find_all('input')[1]['value']
            
            # If presence button does not exist, presence failed (status code PRESENCE_FILLED)
            if(class_html.find('button', {"name": "form[tidakhadir]"})):
                logging.info(f'{RequestCodeMessage.PRESENCE_FILLED} for {c["name"]}')
                fail_callback(RequestCode.PRESENCE_FILLED)
                return (RequestCode.PRESENCE_FILLED, RequestCodeMessage.PRESENCE_FILLED, c["name"])

            # Try filling the presence form
            presence_data = {
                "form[hadir]": "",
                "form[returnTo]": class_link["href"].strip(),
                "form[_token]": class_token,
            }
            result = session.post(f'https://akademik.itb.ac.id{class_action}', presence_data)

            # Presence form filled (status code SUCCESS)
            logging.info(f'{RequestCodeMessage.SUCCESS} for {c["name"]}')
            success_callback()
            return (RequestCode.SUCCESS, RequestCodeMessage.SUCCESS, c["name"])

    # There's currently no class (status code NO_CLASS)
    logging.info(RequestCodeMessage.NO_CLASS)
    fail_callback(RequestCode.NO_CLASS)
    return (RequestCode.NO_CLASS, RequestCodeMessage.NO_CLASS, None)
