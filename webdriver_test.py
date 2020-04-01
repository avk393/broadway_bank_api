from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.by import By
import sys
import pandas as pd
import time
import csv




if(len(sys.argv)<3):
	print("Please enter your username and password when running script")
	sys.exit()
username = sys.argv[1]
pwd = sys.argv[2]

URL = 'https://broadway.bank/'
driver = webdriver.Safari()
driver.set_window_size(1080, 920)
driver.get(URL)

#user_entry = WebDriverWait(driver, 5).until(ExpectedConditions.element_to_be_clickable((By.ID,'uName')))
user_entry = driver.find_element_by_id('uName')
password_entry = driver.find_element_by_id('pWord')
user_entry.click()
user_entry.send_keys(username)
password_entry.click()
password_entry.send_keys(pwd)
password_entry.send_keys(Keys.ENTER)

time.sleep(10)
save = driver.find_element_by_xpath('//*[@id="M_layout_content_PCDZ_M4HNZU6_ctl00_webInputForm_btnSave"]')
save.send_keys(Keys.ENTER)

time.sleep(5)
account = driver.find_element_by_xpath('//*[@id="accountSummaryController_c"]/div[1]/div/ul/li[2]/label/div/div[1]/span/span[1]')
account.click()

time.sleep(5)
try:
	table = driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div[3]/div[1]/div[4]/div[6]/div[3]/div[5]/div[2]/div/div[4]/table[2]/tbody')
	for row in table.find_elements_by_xpath('.//tr'):
		for cell in row.find_elements_by_xpath('.//td'):
			print(cell.text)
except Exception as err:
	print(err)

driver.quit()


"""
*** Make a csv file with all the info
*** Find an already trained model to make predictions for classifying bank charges, and if possible, predicting future expenditures
*** Find GUI API to display info
*** push to github
*** argument: filename, start date, end date

#creating csv file, writing data
if(len(sys.argv) > 0 ):
	#open csv file, write data to it
"""