from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from enum import Enum
import time
import re

import logging
logging.basicConfig(format='[%(asctime)s] - %(message)s', datefmt='%d %b %H:%M:%S', level=logging.INFO)

class Code(Enum):
    DRIVER_INIT_ERROR = 0
    INVALID_LOGIN = 1
    NO_CLASS = 2
    PRESENCE_NOT_OPENED_YET = 3
    SUCCESS = 4
    PRESENCE_ALREADY_FILLED = 5


message = {
    Code.DRIVER_INIT_ERROR: "Failed to init driver",
    Code.INVALID_LOGIN: "Invalid password",
    Code.NO_CLASS: "There's currently no class",
    Code.PRESENCE_NOT_OPENED_YET: "Presence form not opened yet",
    Code.SUCCESS: "Presence form filled successfully",
    Code.PRESENCE_ALREADY_FILLED: "Presence form already filled",
}
def presence(username, password, success_callback=lambda: None, fail_callback=lambda: None, delay=8, headless=True, options=None):
    code = Code.DRIVER_INIT_ERROR
    classcode = ""

    # Presence
    try:
        # Preparing webdriver
        logging.info('Preparing webdriver')
        if options is None:
            options = Options()
            if(headless):
                options.add_argument("--headless")
        args = {
            "options": options,
        }

        # Opening webdriver
        logging.info('Opening webdriver')
        driver = None
        cnt = 0
        error = None
        while driver is None and cnt < 10:
            try:
                driver = webdriver.Firefox(**args)
                break
            except Exception as e:
                cnt += 1
                error = e
        else:
            logging.error("Fail to init webdriver after retrying " + str(cnt) + " times | " + str(error))
            raise error

        # Presencing...
        code, classcode = presence_util(driver, username, password, delay)
        if code == Code.SUCCESS:
            success_callback(classcode, message[code])
        else:
            fail_callback(code, classcode, message[code])

    except Exception as exc:
        logging.exception(exc)
    finally:
        if driver is not None:
            driver.quit()
        return (code, classcode, message[code])

def presence_util(driver, username, password, delay):
    driver.implicitly_wait(0.1)

    # INA Login page
    logging.info('Opening INA login site')
    driver.get('https://login.itb.ac.id/cas/login?service=https%3A%2F%2Fakademik.itb.ac.id%2Flogin%2FINA')
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_xpath('//input[@type=\'submit\']').click()

    # SIX Dashboard
    logging.info('Opening SIX dashboard')
    fullhtml = driver.find_elements_by_tag_name('body')[0].get_attribute('innerHTML')
    try:
        _ = re.search(".*mahasiswa:(.*?)/.*?", fullhtml).group(1)  # nim
    except Exception:
        return (Code.INVALID_LOGIN, "")
    class_link = driver.find_elements_by_xpath("//div[contains(@class, 'apps')]//div[contains(@class, 'col-xs-4 col-sm-3 col-md-2 text-center')]")[3]
    class_link.click()

    # SIX Class Menu
    logging.info('Opening SIX class menu')
    current_day_cell = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'bg-info')))
    classes_today = current_day_cell.find_elements_by_xpath('.//div/div[@title]/a')
    classes_schedule = list(map(lambda val: re.sub(r'(..:..-..:..).*', r'\1', val.text).split('-'), classes_today))
    classes_code = list(map(lambda val: val.text[12:], classes_today))

    # Get current server time (GMT +7)
    t = time.gmtime(time.time() + 25200)
    current_time = time.strftime("%H:%M", t)
    logging.info('Current server time: {}'.format(current_time))

    # Input presence current z`attended class
    for index, schedule in enumerate(classes_schedule):
        # Get schedule time
        start_time, end_time = schedule[0], schedule[1]

        if(start_time <= current_time <= end_time):
            logging.info('Checking {}'.format(classes_code[index]))
            classes_today[index].send_keys(Keys.ENTER)

            # Wait until finished loading
            WebDriverWait(driver, delay).until(EC.invisibility_of_element((By.XPATH, "//*[contains(@class, 'loading')]")))

            # Checking for unpresence button
            try:
                _ = driver.find_element_by_id('form_tidakhadir')
                logging.info('Presence form is filled for {}'.format(classes_code[index]))
                return (Code.PRESENCE_ALREADY_FILLED, classes_code[index])
            except Exception:
                pass

            # Checking for presence button
            try:
                presence_button = driver.find_element_by_id('form_hadir')
                presence_button.click()
                logging.info('Presence successful')
                return (Code.SUCCESS, classes_code[index])
            except Exception:
                logging.info('Presence form currently closed for {}'.format(classes_code[index]))
                return(Code.PRESENCE_NOT_OPENED_YET, classes_code[index])

        else:
            logging.info('Currently is not the time for {}'.format(classes_code[index]))
    return (Code.NO_CLASS, "")
