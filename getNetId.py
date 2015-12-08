from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import pprint
import csv

from progressbar import ProgressBar
from progressbar import Percentage, Bar, ETA

####### FUNCTION OVERVIEW ############
# This function "getNetId()" uses the master csv file to get
# a unique list of employee names from 2014. It uses that list of employee
# names to search the uvm.edu/directory page, renders the javascript inorder
# to unfold the netId containing html. If the netId exists, it will append the
# employee name || netId in a line
# if not, it will add the employee name to a different text file.

def getNetId():
	######### little function to help with searching names
	# given a name in this format: Last,First Middle
	def getLastFirstNames(str_name):
	    last_name = str_name.split(",",2)
	    first_name = last_name[1].split(" ", 2)
	    first_name = first_name[0]
	    last_name = last_name[0]
	    name_search = first_name + " " + last_name
	    return name_search

	########## GET EMPLOYEE NAMES ###########
	# Read in the clean data (csv file) and make a dataframe
	# Use this dataframe and make a list of unique employee names
	df = pd.read_csv(filepath_or_buffer="data/uvm_employee_salary_data_1994-2014.csv")
	# Let's look at just the most recent year
	df = df.loc[df["Year"] == 2014]
	#convert pandas datatype into a unique list
	unique_names = list(set(df.Name))
	#Usefull if I need to breakdown the list
	# unique_names = unique_names[1500:]

	unique_netID = [] # list that stores all the unique netID

	########### SELENIUM DRIVER ##############
	### Use selenium & webdriver to get desired page
	browser = webdriver.Firefox()
	browser.get('http://www.uvm.edu/directory')
	pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(unique_names)).start()
	for i in range(len(unique_names)):
		# create two csv files that selenium results will write into
		# Yes_netId = open("yes_netId.csv", 'w')
		# No_netId = open("no_netId.csv", 'w')
		yes_netId = open("data/Yes_netId_full.txt", 'a')
		no_netId = open("data/No_netId_full.txt", "a")

		# get employee search term name using previous function
		search_name = getLastFirstNames(unique_names[i])
		try:
			browser.get('http://www.uvm.edu/directory')
			elem = browser.find_element_by_name('directory_name') # Find the search box
			elem.send_keys(search_name + Keys.ENTER)
			# Have the program wait for 2 seconds for the javascript to laod
			time.sleep(2)   
			element = browser.find_element_by_xpath("//td[@data-label='NetID']")
			search = element.text
			#### write to a csv file
			# print search
			yes_netId.write(unique_names[i])
			yes_netId.write(" || ")
			yes_netId.write(search)
			yes_netId.write("\n")
		except:
			### write to a csv file
			no_netId.write(unique_names[i])
			no_netId.write("\n")

		# close the two csv files
		no_netId.close()
		yes_netId.close()
		pbar.update(i+1)
	pbar.finish()

	browser.quit()


### call function
getNetId()
