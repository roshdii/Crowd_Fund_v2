######################################
###### STANDALONE FUNCTIONS ##########
######################################	
import re
import os 
import csv
import getpass 
email_regex = '\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+'
mob_regex = "01[0125][0-9]{8}"

def check_email(x):      
	if(re.match(email_regex,x)) != None :
		return 1 
	else :
		return 0 
def check_str(x):
	for i in x :
		if i.isdigit() and i != '':
			return  0
	return 1
def check_num(x):
	for i in x :
		if not i.isdigit():
			return  0 
	return 1
def check_mob(x):
	if 	re.match(mob_regex,str(x)) != None :
		return 1 
	else :
		return 0
#########################################
def enter_name():
	while True:
		name = input("Enter  name :")
		if check_str(name) :
			print("Valid Name ")
			break
		else:
			print("Invalid Name ")
	return name 
###########################################
def enter_age():
	while True:
		age = input ("Enter  age :")
		if check_num(age) :
			if int(age) >= 0 and int(age) <= 150 :
				print("Valid age")
				break
			else :
				print("Invalid age")	
		else:
			print("Invalid age")
	return age 
###########################################
def enter_email():	
	while True:
		email = input ("Enter  email :")
		if check_email(email) :
			print("Valid email")
			break
		else:
			print("Invalid email")
	return email
###########################################
def enter_mobile():
	while True:
		mobile = input ("Enter  mobile :")
		if check_num(mobile) : 
			if check_mob(mobile):
				print("Valid mobile")
				break
			else:
				print("Invalid mobile number")
		else :
				print("Invalid  number")
	return mobile
###########################################
def enter_address():
	while True:		
		address = input ("Enter  address :")
		if check_str(address) :
			print("Valid address")
			break
		else:
			print("Invalid address")
	return address
############################################
def enter_pass(iter=2):
	while True :
		x = getpass.getpass("Please Enter Password : ")
		if iter == 1 :
			return x 
		y = getpass.getpass("Enter the same password Again : ")
		if x == y :
			return x 
		else:
			input("you enter different passwords !! ")
###########################################
def enter_decimal(strrrr):
	while True : 
		x = input(strrrr)
		if check_num(x) :
			return x 
		else :
			print("Not A Number , plz enter it again ")
###########################################
###### END OF STANDALONE FUNCS ############
###########################################

##############################################################
def check_dir(db_dir_name):
	try :
		l = os.listdir(db_dir_name)
		if len(l) > 0 :
			print("Done checking db/ no. of files = ",len(l))
	except FileNotFoundError:
		print("Error in accessing Database directory !!! Creating New db ")
		os.mkdir(db_dir_name)

def check_file(db_dir_name,db_file,dict_header):
	try :
		# check file is exist 
		x = open(db_dir_name+"/"+db_file,'r')
		x.close()
	except:
		# create new file if not exist 
		n = open(db_dir_name+"/"+db_file,'a')
		writer = csv.DictWriter(n, fieldnames=dict_header)
		writer.writeheader()
		n.close()

def clear_screen():
	os.system('clear')