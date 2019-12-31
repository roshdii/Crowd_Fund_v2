#! /usr/bin/env python3.6
## File : Crowd Funding Donating System 
## Author : Eslam Roshdi 
## Email : e.roshdii@gmail.com
## Date : 21 Nov 2019
## Info : e.g kick starter 
## Course : Intro to python
## Instructor : Abd Arahman Hamdy 
import sys 
print(sys.version)
import cv2
print(cv2.__version__)
import os 
from checking_funcs import *
from menu_class import MENU
import numpy as np

db_dir = "db"
user_file = "user.csv"
proj_file = "proj.csv"
dont_file = "dont.csv"

user_file_header = ['id','name','email','pswd','img','mobile','dont']
proj_file_header = ['id','name','u_id','total','donats','st_date','end_date','category','details','tags']
dont_file_header = ['id','p_id','u_id','amount']

class User:
	# List of Users
	# add user , delete, edit, view 

	users = []
	no_of_users = 0
	menu = MENU(['View Info','Edit info','Delete Account'])
	edit_menu = MENU(['name','email','password','image','mobile'])

	def __init__(self,id,name,email,pswd,img,mobile,dont):
		# check values & assign
		# add(self)
		print("construct user")
		self.id = id  
		self.name = name 
		self.email = email 
		self.pswd = pswd
		# self.projects = []
		self.img = img
		self.mobile = mobile
		self.dont = int(dont) 
					
	@classmethod
	def add(cls,**kwargs):
		# append(self) to list 
		# recursive update 
		print("user add")
		if len(kwargs) == 0 :
			tmp_dic = {
				'id' : (cls.no_of_users+1) ,
				'name' : enter_name() , 
				'email' : enter_email(),
				'pswd' : enter_pass() , #input("Enrer password : "),
				'img' : 0,
				'mobile':enter_mobile(),
				'dont' : 0 
			}
		else :
			tmp_dic = kwargs 

		for obj in cls.users :
			if obj.email == tmp_dic['email'] :
				return -1 

		X = cls(**tmp_dic)
		if X.img == 0 :
			X.img_write() 
			X.img = 1

		cls.users.append(X)
		cls.no_of_users += 1
		cls.recursive_update_users()
		return X 
	

	def edit(self):
		print("user edit")
		# display all info
		# edit whatever 
		# recursive update 
		while True :
			clear_screen()
			self.view()
			x = User.edit_menu.draw()
			if x == 1 :
				print("Enter new name ")
				self.name = enter_name()
			elif x == 2 : 
				print("Enter new email : ")
				self.email = enter_email()
				# consider change to a preserved one 
			elif x == 3 : 
				self.pswd = enter_pass() #input("Enter new password : ")
			elif x == 4 : 
				self.img_write()
				self.img = 1
			elif x == 5 :
				self.mobile = enter_mobile()
			elif x == 0 :
				break ;
			else : 
				print("invalid")
		User.recursive_update_users()

	def delete(self):
		print("user delete")
		# remove user obj from list 
		# recursice update 
		if input("Are you sure to delete you Account ?[Y/N]") == 'Y' :
			x = input("Enter your password : ")
			if x == self.pswd :
				User.users.remove(self)
				self.img_delete()
				for p in Project.projects : 
					if int(p.u_id) == int(self.id) :
						p.end(su=1)
				User.recursive_update_users()
				input("Account Removed")
				return 1 

			else :
				input("Invalid password ")

	def view(self):
		print("user view")
		# display current user info
		print("ID : ",self.id)
		print("Name : ",self.name)
		print("Email : ",self.email)
		print('Mob : ',self.mobile)
		print("Don : ",self.dont)
		self.img_read()
	def add_dont(self,d):
		self.dont += d 
		
	def img_write(self):	
		cap = cv2.VideoCapture(0)
		print("Take a pricture [press q in the frame to save your pic ]")
		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()

			# Our operations on the frame come here
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			scale_percent = 50 # percent of original size
			width = 160 #int(gray.shape[1] * scale_percent / 100)
			height = 160 #int(gray.shape[0] * scale_percent / 100)
			dim = (width, height)
			# resize image
			resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
			 
			# Display the resulting frame
			cv2.imshow('frame',resized)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cv2.imwrite('db/'+str(self.id)+'.jpg',resized) 
				break

		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()

		return resized
	
	def img_read(self):
		# print(self.img)
		# input(self.name)
		if int(self.img) == 1 :
			# print("self.img == 1 ")
			try :
				im_file_name = 'db/'+str(self.id)+'.jpg'
				im = cv2.imread(im_file_name)
				cv2.imshow(im_file_name,im)
				cv2.waitKey(2) 
				# while True :
					# if cv2.waitKey(1) & 0xFF == ord('q') or input():
						# break;
				input("Enter any key ")
				cv2.destroyAllWindows()

			except Exception as e :
				print(e)
		else :
			print(" No self img ")

	def img_delete(self):
		if self.img == 1 :
			os.remove('db/'+str(self.id)+'.jpg')


	@classmethod
	def login(cls,email,psw):
		print("user select")
		# search for user with email 
		# check for psw 
		# return user obj if ok 
		# return -1 if not ok
		for obj in cls.users:
			if obj.email == email and obj.pswd == psw :
					return obj
		return -1 
	########### FILE ######################
	@classmethod
	def recursive_read_users(cls):
		print("users recursive read ")
		# check db file is exit if not make a new 
		# read users file db 
		# convert to user obj 
		# append obj to users list 
		check_file(db_dir,user_file,user_file_header)
		with open(db_dir+'/'+user_file,'r') as file :
			txt_reader = csv.DictReader(file)
			for line in txt_reader :
				usr = dict(line)
				cls.add(**usr)

	@classmethod
	def recursive_update_users(cls):
		print("users recursive update ")
		# check db file is exit if not make a new 
		# loop users list 
		# convert from obj to dict 
		# write to users file 
		check_file(db_dir,user_file,user_file_header)
		with open(db_dir+'/'+user_file,'w') as file :
			txt_writer = csv.DictWriter(file,fieldnames=user_file_header)
			txt_writer.writeheader()
			for obj in cls.users:
				tmp_dic = {
					'id' : obj.id,
					'name':obj.name,
					'email':obj.email,
					'pswd':obj.pswd,
					'img':obj.img,
					'mobile':obj.mobile,
					'dont' : obj.dont
				}
				txt_writer.writerow(tmp_dic)



class Project:
	# List of Projects 
	# Start Project (with st.date / end.date) 
	# End Project (check donation 25% reached)

	projects = []
	no_of_projects = 0 
	menu = MENU(['Add Project','donate projct','Edit Project','Delete Project','View project','View Project of user','View Projects by date','View All Projects'])
	edit_menu = MENU(['name','end_date','category','details','tags'])

	proj_menu = MENU(projects)

	def __init__(self,id,name,u_id,total,donats,st_date,end_date,category,tags,details):
		print("construct project ")
		# check_values & assign them 
		# start project 
		self.id = int(id)
		self.name = name 
		self.u_id = int(u_id)
		self.total = int(total) #target 
		self.donats = int(donats) 
		self.st_date = st_date
		self.end_date = end_date
		self.category = category 
		self.details = details 
		self.tags = tags 

	@classmethod
	def add(cls,**kwargs):
		print("add project ")
		# take values 
		# append to list 
		# recursive update project file 
		 
		for obj in cls.projects :
			if obj.id == kwargs['id'] :
				input("Project found before !!")
				return -1 

		X = cls(**kwargs)
		cls.projects.append(X)
		cls.no_of_projects += 1 
		cls.recursve_update_projects()
		cls.menu_update()
		return X 

	@classmethod
	def start(cls,u_id,name=None):
		print("project start")
		# recieve info about project from user 
		if name == None : 
			name = input("Enter projct name : ") 

		tmp_dic = {
			'id' : cls.no_of_projects+1 ,
			'name' : name ,
			'u_id' : u_id,
			'total' : enter_decimal("Enter total target : "),# int(input("Enter total target : ")) ,
			'donats' : 0 ,
			'st_date':input("Enter start date of campaign [dd-mm-yyyy]: "),
			'end_date':input("Enter end date of campaign [dd-mm-yyyy]: "),
			'category':0,#input("Enter Category : "),
			'details':0,#input("Enter details of project : "),
			'tags':0 ,#input("Enter tags : "),

		}
		# return tmp_dic 
		return cls.add(**tmp_dic)
	
	@classmethod 
	def select_by_user_id(cls,u_id):
		print("project select ")
		lis = []
		for pro in cls.projects : 
			if pro.u_id == u_id :
				print(pro.name)
				lis.append(pro)
		return lis  

	@classmethod 
	def select_by_id(cls,id_):
		print("project select ")
		lis = []
		for pro in cls.projects : 
			if pro.id == id_ :
				# print(pro.name)
				lis.append(pro) 
		return lis 


	def donate(self):
		print("project donate")
		# construct donate with id of user & project
		print("Current total donation of project : ",self.donats," & Total Needed donations = ",self.total)
		x= input("Enter donation value : ")
		try :
			if x.isdigit() :
				self.donats = int(self.donats) +  int(x) 
				Project.recursve_update_projects()
				return x
			else : 
				input("Not digit ")
		except :
			input("Error enter value ")

	def edit(self):
		print("project edit")
		# edit details of project 
		# recursive update 
		d = Project.edit_menu.draw()
		if d == 1 : 
			self.name = input("Enter the new name : ")
		elif d == 2 :
			self.end_date = input("Enter the new date [dd-mm-yyy] : ")
		elif d == 3 : 
			self.category = input("Enter the new category : ")
		elif d == 4 : 
			self.details = input("Enter the new details : ")
		elif d == 5 : 
			self.tags = input("Enter te new tags : ")
		else : 
			print("Invalid Enterd ")

		Project.recursve_update_projects()

	def end(self,su=0):
		print("project end")
		# check 25% off and time not passed
		# remove project from list
		# recursive update project file
		
		if su == 0  and self.donats >= (self.total/4 ):
			print("current donation : ",self.donats,"target  : ",self.total)
			input("Can't delete this project [ enter any key to continue ] ")
			return 
		if su == 1 or input("Are your sure to end this project ? [Y/N]")  == 'Y' :
			Project.projects.remove(self)
			Project.no_of_projects -= 1 
			for pro in Project.projects :
				if pro.id > self.id :
					pro.id = pro.id - 1 
			Project.recursve_update_projects()
			Project.menu_update()

	def view(self):
		print("projct view")
		# print all attribuites of this project 
		print("ID : ",str(self.id),end='')
		print("		Name : ",self.name)
		print("		Category : ",self.category)
		print("		Description : ",self.details)
		print("		User Created ID : ", str(self.u_id),end='')
		print("		User Created Name : " , User.users[int(self.u_id)-1].name )
		print("		Current Donations : ",int(self.donats),end='')
		print("		Total needed Donations : ",int(self.total))
		print("		Start Date : ",self.st_date,end='')
		print("		End Date : ",self.end_date)
		print("		Tags : ",self.tags)


	###### Out Sourceing Searching #######
	@classmethod
	def projects_of_user(cls,user_id):
		print("projects of user")
		# display all projects for specific user
		for pro in cls.projects :
			if pro.u_id == user_id :
				pro.view()

	@classmethod
	def projects_of_time(cls,search_date):
		print("projects of time ")
		# display all projects(may inc. donats) within time search 
		if search_date == '' : return 
		s = search_date.split('-')	
		if len(s) != 3 : return  
		s = [int(i) for i in s]

		s = [(s[0]+(s[1]-1)*30),s[2]]
		# print(s)
		for pro in cls.projects :
			p_st = pro.st_date.split('-') 
			p_st = [int(i) for i in p_st]
			p_st = [p_st[0]+(p_st[1]-1)*30 , p_st[2]]

			p_en = pro.end_date.split('-') 
			p_en = [int(i) for i in p_en]
			p_en = [p_en[0]+(p_en[1]-1)*30 , p_en[2]]
			# print(pro.name,pro.st_date,pro.end_date)			
			# print(p_st)
			# print(p_en)
			# print(s)
			if (s[1] < p_en[1] and s[0] >= p_st[0]):
				pro.view()
				# print('1')
			elif (s[1] == p_st[1] and s[0] <= p_en[0] and s[0] >= p_st[0] ) :
				pro.view()
				# print('2')
			elif (s[1] >= p_st[1] and s[0] <= p_en[0]) :
				pro.view()
				# print('3')
			
	@classmethod
	def all_projects(cls):
		print("all projects ")
		# display all projects 
		for pro in cls.projects : 
			pro.view()

	########### FILE ######################
	@classmethod
	def recursive_read_projects(cls):
		print("projects recursive read")
		# check db file is exit if not make a new 
		# read projects file db 
		# convert to project obj 
		# append obj to projects list 
		check_file(db_dir,proj_file,proj_file_header)
		with open(db_dir+'/'+proj_file,'r') as file :
			txt_reader = csv.DictReader(file)
			for line in txt_reader :
				pro = dict(line)
				cls.add(**pro)

	@classmethod
	def recursve_update_projects(cls):
		print("projects recursive update")
		# check db file is exit if not make a new 
		# loop projctss list 
		# convert from obj to struct 
		# write to projects file 
		check_file(db_dir,proj_file,user_file_header)
		with open(db_dir+'/'+proj_file,'w') as file :
			txt_writer = csv.DictWriter(file,fieldnames=proj_file_header)
			txt_writer.writeheader()
			for obj in cls.projects:
				tmp_dic = {
					'id' : obj.id,
					'name':obj.name,
					'u_id':obj.u_id,
					'total':obj.total,
					'donats':obj.donats,
					'st_date':obj.st_date,
					'end_date':obj.end_date,
					'category':obj.category,
					'details':obj.details,
					'tags':obj.tags,
				}
				txt_writer.writerow(tmp_dic)
	
	@classmethod
	def menu_update(cls):
		cls.proj_menu.edit(cls.projects)

def Signup():
	print("Sign up ")
	#1 Get Info from user(check if valid) 
	#2 Add USer (check return is ok)
	#3 Re #1 if not ok 
	#4 Back to main 
	if User.add() == -1 :
		input("User found before !! [try to login]")
	else :
		input("Sucessfully SignUp .. try to login")
	
def Login():
	print("Log in")
	l_menu = MENU([])
	errs = 0 
	
	while True :
		clear_screen()
		email = enter_email()
		ps = enter_pass(1)
		loged_user = User.login(email,ps)
		if loged_user == -1 :
			errs += 1 
			if errs >= 3 :
				input("3 Invalid Attempts :: Account Locked !!! ")
				return -1 ; 
			if '0' == input("Invalid login [press to try agian /or/ 0 to exit] : "+"\n"):
				return 0
		else :
			input("Successfully login Hi "+loged_user.name)
			break 

	clear_screen()
	loged_user.view()
		
	while True :			
		clear_screen()
		re1 = acco_menu.draw()
		if re1 == 1 :
			while True :
				clear_screen()
				re2 = User.menu.draw()
				if re2 == 1 :
					loged_user.view()
					input("Enter any key to continue ")
				elif re2 == 2 :
					loged_user.edit()
				elif re2 == 3 :
					x = loged_user.delete()
					if x == 1 : 
						return ;
				elif re2 == 0 :
					break;
				else :
					print("Invalid ")

		elif re1 == 2 :
			
			while True :
				clear_screen()
				re2 = Project.menu.draw()
				if (re2 == 1 or re2 == 6 or re2 == 7 or re2 == 8 ):
					if re2 == 1 :
						ProX = Project.start(loged_user.id)
						# continue ; 
					elif re2 == 6 :
						ss = input("Enter user id : [0 for current user ]")
						try :
							if ss.isdigit()  :
								if int(ss) == 0 : 
									ss = loged_user.id 
								print(ss)
								Project.projects_of_user(int(ss))
								# input()
						except :
							input("Invalid user id ")
						# continue ;
					elif re2 == 7 : 
						ss = input("Enter start date [dd-mm-yyyy] : ")
						Project.projects_of_time(ss)
						# input()
						# continue ;
					elif re2 == 8 :
						Project.all_projects()
						# input()
						# continue ;
					input("Enter any key to continue ")
					continue

				elif (re2 == 3 or re2 == 4 ):
					l = Project.select_by_user_id(int(loged_user.id))
					clear_screen()
					l_menu.edit([i.name for i in l])
					x = l_menu.draw()

					if x == 0 or x == -1 :
						continue 

					
					if re2 == 3 :
						l[x-1].edit()
					elif re2 == 4 : 
						l[x-1].end()


				elif (re2 == 2 or re2 == 5 ):
					l = Project.projects 
					clear_screen()
					l_menu.edit([i.name for i in l])
					x = l_menu.draw()

					if re2 == 2 :
						cudo = l[x-1].donate()
						input(cudo)
						loged_user.add_dont(int(cudo)) 
					elif re2 == 5 :
						l[x-1].view()
						input()
				
				elif re2 == 0 :
					break;

				else :
					print("Invalid ") 

		elif re1 == 3 :
			print("Sign out")
			break;

		else :
			print("invalid")
	#1 check email/pass for user >> if true login_user is selected  
	#2 User menu : Account settings , Projects , Donations , Signout
	#3 Account Setting menu : Edit Info , Delete Account 
	#4 Project Menu : Add project(with data) , view projects(user/all/data) , edit project , Delete project , 
	#5 Donation Menu : project list (donate project / delete donate )
	#6 Sign Out 

main_menu = MENU(['Signup','Login','Exit'])
acco_menu = MENU(['Account','Projects','Signout'])

def main():
	
	#1 main menu : Signup , login 
	#2 signup > go for signup 
	#3 login > go for login 
	#4 Exit 
	check_dir(db_dir)
	User.recursive_read_users()
	Project.recursive_read_projects()

	while True :
		clear_screen()
		re1 = main_menu.draw()
		if re1 == 1 :
			Signup()
		elif re1 == 2 :
			if Login() == -1 :
				return -1
		elif re1 == 3 :
			return 0 ; 
		else :
			print("Invalid")

if __name__ == "__main__":
	main()

# class Donation:
# 	# List of donations 
# 	# add a donate with the project id & user id donating 
# 	# remove a donate (at specfic project / from login user)
	
# 	dontas = []
# 	no_of_donats = 0 
# 	menu = MENU(['add','donates of user','donats on project'])

# 	def __init__(self,donate_id,project_id,user_id,total_donat):
# 		print("construct donate")
# 		if donate_id == None :
# 			donate_id = no_of_donats + 1  
# 		# check & assign values to current donation
# 		# add (self)
# 		self.id = donate_id 
# 		self.u_id = user_id 
# 		self.p_id = project_id 
# 		self.total_donates = self.total_donates  + total_donat

# 	@classmethod
# 	def add(cls,d_id,p_id,u_id,total_dona):
# 		print("donat add ")
# 		# append donate_obj to list 
# 		# recursive update donate file 
# 		x = cls(d_id,p_id,u_id,total_dona)
# 		cls.donates.append(x)
# 		Donation.recursve_update_donats()

# 	def remove(Self):
# 		print("donat remove")
# 		# remove donate with id from list 
# 		# recursive update donate file


# 	########## out sourceing search ####################
# 	@classmethod 
# 	def donats_of_user(cls,user_id):
# 		print("donats of user")
# 		#search for all donats with user_id 
# 		#display donats and prespective projects

# 	@classmethod
# 	def donats_on_project(cls,project_id):
# 		print("donats on project")
# 		#search for all donats with project_id 
# 		#display donats and prespective user 

# 	########### FILE ######################
# 	@classmethod
# 	def recursive_read_donats(cls):
# 		print("donats recursrive read")
# 		# check db file is exit if not make a new 
# 		# read donate file db 
# 		# convert to donate obj 
# 		# append obj to donats list 

# 	@classmethod
# 	def recursve_update_donats(cls):
# 		print("donats recursrive update ")
# 		# check db file is exit if not make a new 
# 		# loop donats list 
# 		# convert from obj to struct 
# 		# write to donate file 
# 		check_file(db_dir,donat_file,donat_file_header)
# 		with open(db_dir+'/'+donat_file,'w') as file :
# 			txt_writer = csv.DictWriter(file,fieldnames=donat_file_header)
# 			txt_writer.writeheader()
# 			for obj in cls.donates:
# 				tmp_dic = {
# 					'id' : obj.id,
# 					'u_id':obj.name,
# 					'p_id':obj.u_id,
# 					'total':obj.total,
# 					'donats':obj.donats,
# 				}
# 				txt_writer.writerow(tmp_dic)
