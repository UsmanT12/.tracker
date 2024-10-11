#file that find all the urls necessary to create database
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from players import *
from General_Funcs import *

schedule_url = 'https://www.wnba.com/schedule?season=2024&month=all'
path = '/Users/usmantahir/Github_Clones/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get(schedule_url)

WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, ''))
)

boxscore_link = driver.find_element(By.CLASS_NAME, '')
arr = [element.text for element in boxscore_link]
print(arr)
#team_names_text = [team.text for team in team_names]