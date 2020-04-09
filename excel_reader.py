import sys
import csv
import pandas as pd
import matplotlib.pyplot as plot
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


arguments = 3
date_format = 3

# returns FALSE if user entered date format improperly
def check_input_format(date):
	global date_format
	if len(date)!=date_format:
		return False

	month = date[0]
	day = date[1]
	year = date[2]
	# add a check later to see if it's a leap year
	if int(month)==2 and int(day)>28:
		return False;
	if int(month)<1 or int(month)>12:
		return False
	if int(day)<0 or (int(month)%2==0 and int(day)>30) or (int(month)%2==1 and int(day)>31):
		return False
	if len(year)!=4:
		return False

	return True

# puts date in day/month/year order
def format_date(date):
	global date_format
	#error checking --> return as is if not correct format
	if len(date)!=date_format:
		return date

	temp = []
	for i in date:
		temp.append(i)
	tmp = date[0]
	temp[0] = date[1]
	temp[1] = tmp
	return temp

""""
*** pass in two arrays, [day,month,year]
*** returns:
		 0 if first parameter is more recent, 
		 1 if second parameter is more recent,
		 2 if they're the same
		 -1 if the format of either parameter is incorrect
"""
def compare_dates(fd,sd):
	global date_format
	if len(fd)!=len(sd)!=date_format:
		return -1

	i = len(fd)-1
	#print(fd)
	#print(sd)
	while i>=0:
		if (type(fd[i]) or type(sd[i]))!=int:
			#print("return -1")
			return -1
		elif fd[i]>sd[i]:
			#print("return 0")
			return 0
		elif fd[i]<sd[i]:
			#print("return 1")
			return 1
		i -= 1
	#print("return 2")
	return 2	

def webscrape(browser, charge_info):
	# formatting bank charge description for google to digest it easier
	charge_descr = charge_info[4:]
	if 'VIS' in charge_descr:
		i = charge_descr.index('VIS')
		charge_descr = charge_descr[0:i]

	browser.implicitly_wait(3)
	browser.get('https://google.com')
	browser.implicitly_wait(3)
	search_form = browser.find_element_by_xpath("//input[@name='q']")
	search_form.send_keys(charge_descr)
	search_form.submit()

	browser.implicitly_wait(3)
	try:
		results = browser.find_elements_by_class_name('YhemCb')
		classification = results[1].text
		if 'bar' or 'restaurant' or 'lounge' in classification:
			print(charge_descr, classification)
			return True
		else:
			return False

	except Exception:
		return False
	




def main(): 

	statement = pd.read_csv('export_20200402.csv')
	data = statement.drop(['Comments','Check Number'], axis=1)
	#print(data.to_string())
	# most recent date on spreadsheet
	max_date = data.max()['Date'].split('/')
	# earliest date on spreadsheet
	min_date = data.min()['Date'].split('/')
	max_date = [int(i) for i in max_date]
	min_date = [int(i) for i in min_date]
	start_date = min_date
	end_date = max_date

	if len(sys.argv)==date_format:
		#add error handling here
		start_date = sys.argv[1].split('/')
		end_date = sys.argv[2].split('/')
		if (check_input_format(start_date) and check_input_format(end_date)) == False: 
			print("Please enter valid dates in the following format: Month/Day/Year")
			sys.exit()
			
		start_date = [int(i) for i in start_date]
		end_date = [int(i) for i in end_date]
		if compare_dates(format_date(start_date),format_date(max_date))==0 or compare_dates(format_date(end_date),format_date(min_date))==1:
			print("Don't have the data for these dates")
			sys.exit()
		if compare_dates(format_date(start_date), format_date(min_date)) == 1:
			start_date = min_date
			print("Earliest date on record is: ", start_date)
		if compare_dates(format_date(end_date), format_date(max_date)) == 0:
			end_date = max_date
			print("Most recent date on record: ", end_date)

	# filtering out dates user didn't ask for
	# filtering to match start date
	to_drop = []
	for i in list(data.index):
		temp_date = data.iloc[i]['Date'].split('/')
		data_date = [int(z) for z in temp_date]
		if compare_dates(format_date(start_date),format_date(data_date))!=0:
			break
		to_drop.append(i)
	# filtering to match end date
	for j in reversed(list(data.index)):
		temp_date = data.iloc[j]['Date'].split('/')
		data_date = [int(z) for z in temp_date]
		if compare_dates(format_date(end_date),format_date(data_date))!=1:
			break
		to_drop.append(j)

	if len(to_drop) > 0:
		data = data.drop(to_drop)
	#print(data)


	# need to include charges on credit card statement also later
	# categorizing data 
	charge_categories = ['Rent/Utilities', 'Venmo', 'Groceries', 'GasStation', 'Restaurants', 'Miscellaneous']
	grouped_charges = pd.DataFrame(index=[0])
	for cat in charge_categories:
		grouped_charges[cat] = float(0)

	# initializing browser to check restaurants
	opts = Options()
	opts.set_headless()
	assert opts.headless  # Operating in headless mode
	browser = Firefox(executable_path=r"/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver", options=opts)

	for i in range(len(data)):
		charge_amount_str = data.iloc[i]['Amount'].replace(',','')
		charge_info =  data.iloc[i]['Description']
		if '-' in charge_amount_str:
			charge_amount = float(charge_amount_str[2:])
			if "MAA" in charge_info or "City of Austin" in charge_info:
				grouped_charges.at[0, 'Rent/Utilities'] = grouped_charges.iloc[0]['Rent/Utilities']+charge_amount
			elif "H-E-B" in charge_info:
				grouped_charges.at[0, 'Groceries'] = grouped_charges.iloc[0]['Groceries']+charge_amount
			elif "VENMO" in charge_info:
				grouped_charges.at[0, 'Venmo'] = grouped_charges.iloc[0]['Venmo']+charge_amount
			elif "EXXONMOBIL" in charge_info or "SHELL" in charge_info or "ROSEDALE" in charge_info:
				grouped_charges.at[0, 'GasStation'] = grouped_charges.iloc[0]['GasStation']+charge_amount
			elif webscrape(browser, charge_info)==True:
				grouped_charges.at[0, 'Restaurants'] = grouped_charges.iloc[0]['Restaurants']+charge_amount
			else:
				if "IB XFER" in charge_info:
					continue
				#print(charge_info, charge_amount)
				grouped_charges.at[0, 'Miscellaneous'] = grouped_charges.iloc[0]['Miscellaneous']+charge_amount
	
	browser.quit()
	print(grouped_charges)
	




"""
Implement date filter

To classify something as restaurant:
	* search in webdriver
	* scrape to see if resetaurant is mentioned
	* Could potentially use this for gas stations/grocery stores

Use data.loc[data['Amount']># and data.loc[data['Amount']<# to find transactions within certain range]	
Relay data to phone. Be able to see how a purchase will affect budget outlook?
Stripe API for transactions

*** Create a date class at some point
*** Find an already trained model to make predictions for classifying bank charges, and if possible, predicting future expenditures
*** Find GUI API to display info
*** Have user set budget, be able to tell user where they did not meet their goals

https://www.mint.com/

with open('export_20200402.csv') as csvfile:
	reader = csv.reader(csvfile)
	print(reader.line_num)
	categories = next(reader)
	for row in reader:
		print(row)
"""
		


if __name__ == '__main__':
	main()
