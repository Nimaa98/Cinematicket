


import getpass
from noSQL_Database import Nosql_database




class Admin_application():

	Admin_info = {}
	
	def __init__(self,Username,password):
		self.Username = Username
		self.password = password
		
		
	def Set_Username(self,Username):

		if 19<len(Username)<39:

			self.Username = Username

		else:
			raise ValueError
			pass
	
	def Set_password(self,password):
		if 8<len(password)<12:
			self.password = password
		else:
			print('\npassword must have 9 numbers at least\n')
			raise ValueError
	
	
	
	
	@classmethod
	def Sign_up(cls,Username):
	
		
		password = input('\nEnter your password:\n')
		
		instance = cls(Username,password)

		try:
			instance.Set_Username(Username)

			instance.Set_password(password)

			print('\nSign up was done successfully\n')

			cls.Admin_info[Username] = password


			Nosql_database.Add_Admin(cls.Admin_info)

		except ValueError:
			print('\nInvalid input\n')
		
		return True
		
	@staticmethod
	def Login(password):

		entered_password = getpass.getpass('Enter your password:\n')

		if entered_password == password:

			print('\nLogin was done successfully\n')

		else:
			print('incorrect password.\n')





