import sys
import csv
import pandas as pd


arguments = 3
date_format = 3

def formate_dates(date):
	global date_format
	#error checking --> return as is if not correct format
	if len(date)!=date_format:
		return date
	for date_info in date:
		if type(date_info)!=int:
			return date

	tmp = date[0]
	date[0] = date[1]
	date[1] = tmp
	return date

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

	i = len(date_format)
	while i>=0:
		if (type(fd[i]) or type(sd[i]))!=int:
			return -1
		elif fd[i]>sd[i]:
			return 0
		elif fd[i]<sd[i]:
			return 1

	return 2





if(len(sys.argv)<arguments):
	print("Please enter your start date and end date as arguments when running script")
	sys.exit()
#add error handling here
start_date = sys.argv[1].split('/')
end_date = sys.argv[2].split('/')


statement = pd.read_csv('export_20200402.csv')
data = statement.drop(['Comments','Check Number'], axis=1)
#print(data.to_string())
max_date = data.max()['Date'].split('/')
min_date = data.min()['Date'].split('/')





"""
with open('export_20200402.csv') as csvfile:
	reader = csv.reader(csvfile)
	print(reader.line_num)
	categories = next(reader)
	for row in reader:
		print(row)
"""
		