import sys
import csv
import pandas as pd
import matplotlib.pyplot as plot


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



def main(): 

	if(len(sys.argv)<arguments):
		print("Please enter your start date and end date as arguments when running script")
		sys.exit()
	#add error handling here
	start_date = sys.argv[1].split('/')
	end_date = sys.argv[2].split('/')
	if (check_input_format(start_date) and check_input_format(end_date)) == False: 
		print("Please enter valid dates in the following format: Month/Day/Year")
		sys.exit()

	statement = pd.read_csv('export_20200402.csv')
	data = statement.drop(['Comments','Check Number'], axis=1)
	#print(data.to_string())
	# most recent date on spreadsheet
	max_date = data.max()['Date'].split('/')
	# earliest date on spreadsheet
	min_date = data.min()['Date'].split('/')

	max_date = [int(i) for i in max_date]
	min_date = [int(i) for i in min_date]
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
	#indeces = list(data.index)
	separator = -1
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
		data_date = [int(k) for k in temp_date]
		if compare_dates(format_date(end_date),format_date(data_date))!=1:
			break
		to_drop.append(j)

	print(to_drop)
	if len(to_drop) > 0:
		data = data.drop(to_drop)
	print(data)

	#filtering to match end date
	
	#print(data)

	# need to include charges on credit card statement also later
	# categorizing data 
	"""
	charge_categories = ['Rent/Utilities', 'Venmo', 'Groceries', 'GasStation', 'Restaurants', 'Miscellaneous']
	grouped_charges = pd.DataFrame(index=[0])
	for cat in charge_categories:
		grouped_charges[cat] = float(0)

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
			else:
				grouped_charges.at[0, 'Miscellaneous'] = grouped_charges.iloc[0]['Miscellaneous']+charge_amount
	print(grouped_charges)
	"""
	




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

with open('export_20200402.csv') as csvfile:
	reader = csv.reader(csvfile)
	print(reader.line_num)
	categories = next(reader)
	for row in reader:
		print(row)
"""
		


if __name__ == '__main__':
	main()
