class MENU : 

	def __init__(self,menu_list):
		self.inlist = menu_list 
		self.closing_______line = "-----------------"

	def edit(self,menu_li):
		self.inlist = menu_li

	def draw(self):
		print(self.closing_______line)
		idx = 1
		for i in self.inlist:
			print(str(idx)+"- "+i)
			idx+= 1
		print(self.closing_______line)
		return self.get()

	def get(self):
		print("Enter no. or 'identical' Name of item to choose [0 to exit menu ]")
		print(self.closing_______line)
		x = input("-> ")
		# print(str(type(x)) == "<class 'str'>")
		if x == '' : return -1 
		if x == 0 or x == '0' : return 0 
		elif x.isdigit() : 
			x = int(x) 
			if x > 0 and x <= len(self.inlist) :
				# print("i/p = ",x) 
				print("-> Selected Element [ ",self.inlist[x-1]," ]")
				print(self.closing_______line)
				return x
			else :
				input("out of range input ")
				return -1 

		elif str(type(x)) == "<class 'str'>":
			idx = 1 
			for i in self.inlist :
				# print("idx= ",idx,"item= ",i)
				if i == x :
					# print("i/p = ",x)
					print("-> Selected Element [",self.inlist[idx-1]," ]")
					print(self.closing_______line)
					# return str(x)
					return idx
				idx += 1 
		else :
			input("Invalid input for menu items") 
			return -1 