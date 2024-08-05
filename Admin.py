


import getpass
from noSQL_Database import Nosql_database
from datetime import datetime




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

			Admin_application.Account()

		else:
			print('incorrect password.\n')



	@staticmethod
	def Account():

		while True:
			a = input('\nEnter 1 to Add New Movie'
					  '\nor 2 to Delet Movie'
					  '\nor 0 to exit:\n')

			if a == '1':
				New_Movie.Add_Movie()

			elif a== '2':
				Admin_application.Delet_Movie()

			elif a == '0':
				break

			else:
				print('\nInvalid input\n')


	@staticmethod
	def Delet_Movie():

		Movies = Nosql_database.Get_Movies()

		Movies = list(Movies.keys())

		Movies.remove('Movie name')

		print(f'\nThese are Cinema Ticket Movies:\n')

		for i in range(0,len(Movies),3):

			chunk = Movies[i:i+3]

			print(*chunk,sep='          ',end='\n')

		Movie = input('\nEnter the name of the Movie you want to delet:\n')


		if Movie in Movies:
			print('\nEntered movie was daleted.\n')
			Nosql_database.Delet_Movie(Movie)

		else:
			print('\nIncorrect name.try again later\n')



class New_Movie():

	Movie = {}
	Show_times ={}
	first_capacity = {}

	def __init__(self,Movie_latin_name,Movie_farsi_name,Days_num_of_week,
				 Show_times,Capacity,Genre,Price,Permissible_age):


		self.Movie_latin_name ,  self.Movie_farsi_name = Movie_latin_name , Movie_farsi_name
		self.Days_num_of_week ,  self.Show_times = Days_num_of_week , Show_times
		self.Capacity  =  Capacity
		self.Genre , self.Price = Genre , Price
		self.Permissible_age = Permissible_age


	def Set_Movie_latin_name(self,Movie_latin_name):

		for char in Movie_latin_name:
			if (char.isascii() and char.isalpha()) or (char.isascii() and char.isdigit() or char.isspace()):
				continue

			else:
				print('\nInvalid latin name')
				raise ValueError


		self.__class__.Movie[Movie_latin_name] = []

		self.Movie_latin_name = Movie_latin_name

	def Set_Movie_farsi_name(self,Movie_farsi_name):

		persion_range = ((0x0600,0x06FF),(0xFB00,0xFBFF),(0xFE70,0xFEFF),(0x0750,0x077F),(0x08A0,0x08FF))

		for char in Movie_farsi_name:

			code_point = ord(char)
			in_range = False


			for start , end in persion_range:

				if start <= code_point <= end or char.isspace():
					in_range = True
					break

				else:
					continue


			if  not in_range:
				print('\nInvalid farsi name')
				raise ValueError


		self.__class__.Movie[self.Movie_latin_name].append(Movie_farsi_name)

		self.Movie_farsi_name = Movie_farsi_name


	def Set_Show_times(self,times):

		Start_time = times

		show_dict = {'1':"Morning_ShowTime",'2':"Afternoon_ShowTime",'3':"Night_ShowTime"}


		if times.count('') == 3:
			print('\nMovie need at least one show time.\n')
			raise ValueError


		n = 0
		for i in show_dict:

			self.__class__.Show_times[show_dict[i]]= [[],{}]


			Time = New_Movie.Set_Start_time(Start_time[n])

			if Time != '':
				self.__class__.Show_times[show_dict[i]][0].append(Time.hour)
				self.__class__.Show_times[show_dict[i]][0].append(Time.minute)
				self.__class__.Show_times[show_dict[i]].append('Active')

			else:

				self.__class__.Show_times[show_dict[i]][0].append(0)
				self.__class__.Show_times[show_dict[i]][0].append(0)
				self.__class__.Show_times[show_dict[i]].append('Deactive')


			n += 1


		self.Show_times = self.__class__.Show_times


	@staticmethod
	def Set_Start_time(Start_time):

			if Start_time != '':
				try:
					Time = datetime.strptime(Start_time,"%H:%M")
					Time = Time.time()
					return Time

				except ValueError:
					print('\nIncorrect start time')

			else:
				Time = ''
				return  Time


	def Set_Capacity(self,capacity):

		if 0 < int(capacity) <= 400:

			self.Capacity = capacity
		else:
			print('\nInvalid Capacity\n')
			raise ValueError




	def Set_Days_num_of_week(self,Days_num_of_week):

		Days_num_of_week  = Days_num_of_week .split(',')

		Capacity = self.Capacity

		days = []
		days_and_capacity = {}
		celender = {"0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday", "4": "Friday", "5": "Saturday", "6": "Sunday"}

		keys = self.__class__.Show_times.keys()


		for i in Days_num_of_week :
			if i != ',' and 0 <= int(i) <=6:
				day = celender[i]
				days_and_capacity[day] = int(Capacity)
				days.append(int(i))

			elif i == ',':
				continue

			else:
				print('\nInvalid days number')
				raise ValueError


		for i in keys:

			if self.__class__.Show_times[i][2] == 'Active':
				self.__class__.Show_times[i][1] = days_and_capacity
			else:
				continue


		self.__class__.Movie[self.Movie_latin_name].append(days)

		self.__class__.Movie[self.Movie_latin_name].append(self.__class__.Show_times)


		self.Days_num_of_week = Days_num_of_week




	def Set_Genre(self,genre):

		genre_list = ['جنایی', 'اجتماعی/درام', 'اکشن/کمدی', 'ترسناک', 'ترسناک/رازآلود',
					  'تاریخی/درام/عاشقانه', 'خانوادگی/درام', 'کمدی']


		if genre in genre_list:
			self.Genre = genre

			self.__class__.Movie[self.Movie_latin_name].append(genre)

		else:
			print('\nInvalid genre')
			raise ValueError



	def Set_Price(self,price):
		if int(price) > 0:
			self.Price = price
			self.__class__.Movie[self.Movie_latin_name].append(int(price))

		else:
			print('\nInvalid Price')
			raise ValueError

	def Set_Permissible_age(self,age):

		if 0 <= int(age) < 41:
			self.Permissible_age = age
			self.__class__.Movie[self.Movie_latin_name].append(int(age))
			self.__class__.Movie[self.Movie_latin_name].append(int(self.Capacity))


			print('\nMovie added.\n')

			Nosql_database.Add_Movie(self.__class__.Movie)

			self.__class__.Movie = {}


		else:
			print('\nInvalid Age')
			raise ValueError




	@classmethod
	def Add_Movie(cls):
		times =[]

		Movie_latin_name = input('\nEnter the Latin name of the movie:\n')

		Movie_farsi_name = input('\nEnter the Farsi name of the movie:\n')


		Days_num_of_week = input('\nEnter the number of days of the week on which the movie will be played:\n'
								 '\n\n-------------'
							     '\nExample:\n'
							     '\n6, 3, 2, 0\n'
							     '\nNumber of days of the week:\n'
							     '\nMonday: 0, Tuesday: 1, Wednesday: 2, Thursday: 3, Friday: 4,\n'
							     '\nSaturday: 5, Sunday: 6\n'
								 '\n--------------\n')


		print('\n\nwrite the start time of the movie in these show times:\n'
						   'morning show time , afternoon show time , night show time\n'
			  			   '\nIf a show time is inactive, leave the clock blank\n'
						   '\nExample:\n'
						   'morning show time:9:0\n'
						   'afternoon show time:\n'
						   'night show time:20:00'
						   '\n--------------\n')


		morning_show_time = input('morning show time:')
		times.append(morning_show_time)

		afternoon_show_time = input('afternoon show time:')
		times.append(afternoon_show_time)

		night_show_time = input('night show time:')
		times.append(night_show_time)




		Capacity = input('\nEnter the capacity of the movie theater:\n'
						 '\nExample:\n'
						 '\n100\n')


		Genre = input('\nEnter the Genre of the movie:\n'
					     '\n\n------------------'
						 '\nExample:\n'
						 '\nکمدی\n'
						 '\nChoose from the allowed  Genre below:\n'
						 '\n[ جنايي  , اجتماعی/درام , اکشن/کمدی  ,  ترسناک , ترسناک/رازآلود ,'
						 ' کمدی  , خانوادگي/درام  ,  تاريخي/درام/عاشقانه ]'
						 '\n------------\n\n')

		Price = input('\nEnter the Price of the movie theater:\n'
						 '\nExample:\n'
						 '\n80,000\n')


		Permissible_age = input('\nEnter the Permissibleage of the movie theater:\n'
						 '\nExample:\n'
						 '\n18\n')



		instance = cls(Movie_latin_name,Movie_farsi_name,times,Capacity,Days_num_of_week,
					   Genre,Price,Permissible_age)


		user_inputs = {'Set_Movie_latin_name':Movie_latin_name,'Set_Movie_farsi_name':Movie_farsi_name,
					   'Set_Show_times':times,'Set_Capacity':Capacity,
					   'Set_Days_num_of_week':Days_num_of_week,'Set_Genre':Genre,'Set_Price':Price,
			           'Set_Permissible_age':Permissible_age}



		setter_list = ['Set_Movie_latin_name','Set_Movie_farsi_name','Set_Show_times','Set_Capacity',
					   'Set_Days_num_of_week','Set_Genre','Set_Price','Set_Permissible_age']



		for i in setter_list:

			value = user_inputs[i]

			method = getattr(instance,i)

			try:
				method(value)

			except ValueError:

				print('\nTry again')
				break


#New_Movie.Add_Movie()
#New_Movie.Set_Genre('کمدی/اکشن')

#Admin_application.Delet_Movie()