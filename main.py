from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging
import json
import time
import re

logging.basicConfig(format='[%(asctime)s] - %(message)s', datefmt='%d %b %H:%M:%S', level=logging.INFO)

try:
  
  logging.info('Opening webdriver...')
  options = Options()
  options.add_argument("--headless")
  driver = webdriver.Firefox(options=options)

  time.sleep(8)

  # Main page
  logging.info('Opening main site...')
  driver.get('https://akademik.itb.ac.id/')
  driver.find_element_by_id('login').click()

  # Login page
  logging.info('Opening akademik.itb.ac.id login page...')
  driver.find_element_by_xpath('//a[@href=\'/login/INA\']').click()

  # INA login page
  logging.info('Login using ITB SSO...')
  with open('credentials.json', 'r') as f:
    credentials = json.load(f)

  driver.find_element_by_id("username").send_keys(credentials['username'])
  driver.find_element_by_id("password").send_keys(credentials['password'])
  driver.find_element_by_xpath('//input[@type=\'submit\']').click()

  # SIX Dashboard
  logging.info('Opening SIX dashboard....')
  class_link = driver.find_element_by_xpath('//a[contains(@href, \'/app/mahasiswa:{}/kelas\')]'.format(credentials["nim"]))
  driver.execute_script("arguments[0].click();", class_link)

  # SIX Class Menu
  logging.info('Opening SIX class menu....')
  current_day_cell = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'bg-info')))
  classes_today = current_day_cell.find_elements_by_xpath('.//div/div[@title]/a[@class=\'linkpertemuan\']')
  classes_schedule = list(map(lambda val: re.sub(r'(..:..-..:..).*', r'\1', val.text).split('-'), classes_today))

  # Get current time
  t = time.localtime()
  current_time = time.strftime("%H:%M", t)

  # Input presence current attended class
  logging.info('Finding attended class....')
  found = False
  for index, schedule in enumerate(classes_schedule):
    start_time, end_time = schedule[0], schedule[1]
    if(start_time <= current_time <= end_time):
      driver.execute_script("arguments[0].click();", classes_today[index])
      presence_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'form_hadir')))
      presence_button.click()
      logging.info('Presence successful.')
      found=True
      break
  
  if(not found):
    raise Exception('You\'re currently not attending any class.')
  
  # For testing purposes
  # classes_today[0].click()
  # popup_dialog = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role=\'dialog\']')))
  # presence_button = popup_dialog.find_element_by_xpath('.//button[@name=\'form[hadir]\']')
  # presence_button.click()

  # logging.info(classes_schedule)
  # driver.find_element_by_xpath()
except NoSuchElementException as exc:
  logging.exception(
  '''
    Presence failed. Some things are possible:
    > Your class have not opened the presence form yet
    > You have already filled the presence form
    > Your class does not use the SIX presence system
  '''
  )
except Exception as exc:
  logging.exception(exc)
finally:
  time.sleep(5)
  driver.close()
