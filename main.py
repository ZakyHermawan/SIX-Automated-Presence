from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
import re

try:
  driver = webdriver.Firefox()

  # Main page
  print('Opening main site...')
  driver.get('https://akademik.itb.ac.id/')
  driver.find_element_by_id('login').click()

  # Login page
  print('Opening akademik.itb.ac.id login page...')
  driver.find_element_by_xpath('//a[@href=\'/login/INA\']').click()

  # INA login page
  print('Login using ITB SSO...')
  with open('credentials.json', 'r') as f:
    credentials = json.load(f)

  driver.find_element_by_id("username").send_keys(credentials['username'])
  driver.find_element_by_id("password").send_keys(credentials['password'])
  driver.find_element_by_xpath('//input[@type=\'submit\']').click()

  # SIX Dashboard
  print('Opening SIX dashboard....')
  class_link = driver.find_element_by_xpath('//a[contains(@href, \'/app/mahasiswa:{}/kelas\')]'.format(credentials["nim"]))
  driver.execute_script("arguments[0].click();", class_link)

  # SIX Class Menu
  print('Opening SIX class menu....')
  current_day_cell = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'bg-info')))
  classes_today = current_day_cell.find_elements_by_xpath('.//div/div[@title]/a[@class=\'linkpertemuan\']')
  classes_schedule = list(map(lambda val: re.sub(r'(..:..-..:..).*', r'\1', val.text).split('-'), classes_today))

  # Get current time
  print('Opening SIX class menu....')
  t = time.localtime()
  current_time = time.strftime("%H:%M", t)
  print(current_time)

  print('Finding current class....')
  for index, schedule in enumerate(classes_schedule):
    start_time, end_time = schedule[0], schedule[1]
    if(start_time <= current_time <= end_time):
      driver.execute_script("arguments[0].click();", classes_today[index])
      popup_dialog = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role=\'dialog\']')))
      popup_dialog.find_element_by_id('form_hadir').click()
      print('Presence successful.')
      break
  else:
    raise Exception('You\'re currently not attending any class.')
  
  # For testing purposes
  # classes_today[0].click()
  # popup_dialog = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role=\'dialog\']')))
  # presence_button = popup_dialog.find_element_by_xpath('.//button[@name=\'form[hadir]\']')
  # presence_button.click()

  # print(classes_schedule)
  # driver.find_element_by_xpath()
except NoSuchElementException as exc:
  print('Presence failed. Some things are possible:')
  print('> Your class does not use the SIX presence system')
  print('> Your class have not opened the presence form yet')
  print('> You have already filled the presence form')
except Exception as exc:
  print(exc)
finally:
  time.sleep(10)
  driver.close()
