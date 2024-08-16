


import getpass ,logging
from noSQL_Database import Nosql_database
from datetime import datetime
from bank_acounts import Clear_screan




class Admin_application():

	Admin_info = {}

	
	def __init__(self,Username,password):
		self.Username = Username
		self.password = password

		
		
	def Set_Username(self,Username):

		if 19<len(Username)<39:

			self.Username = Username

		else:
			logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن نام نادرست\n')

			raise ValueError

	
	def Set_password(self,password):

		Clear_screan()

		if 8<len(password)<12:
			self.password = password
		else:
			print('\npassword must have 9 numbers at least\n')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن پسورد نادرست\n')

			raise ValueError




	@classmethod
	def Sign_up(cls,Username):

		Clear_screan()

		password = input('\nEnter your password:\n')

		instance = cls(Username,password)

		try:
			instance.Set_Username(Username)

			instance.Set_password(password)

			print('\nSign up was done successfully\n')
			logging.info('ثبت نام ادمین جدیدبا موفقیت انجام شد.\n')

			cls.Admin_info[Username] = password


			Nosql_database.Add_Admin(cls.Admin_info)

		except ValueError:
			print('\nInvalid input\n')

		return True

	@staticmethod
	def Login(password,Username):

		Clear_screan()

		Username = Username[19:]

		entered_password = getpass.getpass('Enter your password:\n')

		if entered_password == password:

			print('\nLogin was done successfully\n')
			logging.info(f'{Username}ورود به حساب کاربری توسط ادمین\n')

			Admin_application.Account()

		else:
			print('incorrect password.\n')



	@staticmethod
	def Account():

		Clear_screan()

		while True:
			a = input('\nEnter 1 to Add New Movie'
					  '\nor 2 to Delet Movie'
					  '\nor 0 to exit:\n')

			if a == '1':
				logging.info(f'اقدام ادمین برای اضافه کردن فیلم به سایت.\n')

				New_Movie.Add_Movie()


			elif a== '2':
				logging.info(f'اقدام ادمین برای حذف کردن فیلم از سایت.\n')

				Admin_application.Delet_Movie()

			elif a == '0':
				logging.info(f'خروج ادمین از حساب کاربری.\n')

				Clear_screan()
				break

			else:
				print('\nInvalid input\n')
				Clear_screan()


	@staticmethod
	def Delet_Movie():

		Clear_screan()

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
			logging.info(f'پاک شدن موفقیت آمیز فیلم از سایت.\n')


		else:
			print('\nIncorrect name.try again later\n')
			logging.warning('.عدم اجرای درخواست ادمین به دلیل وارد کردن نام فیلم به صورت نادرست\n')

			# Clear_screan()



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

		Clear_screan()

		if Movie_latin_name == '':
			print('\nMovie latin name need at least one letter.\n')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه هیچ نام لاتینی وارد نشده است\n')

			raise ValueError


		for char in Movie_latin_name:
			if (char.isascii() and char.isalpha()) or (char.isascii() and char.isdigit() or char.isspace()):
				continue

			else:
				print('\nInvalid latin name')
				logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه نام لاتین فیلم نادرست وارد شده است\n')

				raise ValueError


		self.__class__.Movie[Movie_latin_name] = []

		self.Movie_latin_name = Movie_latin_name


	def Set_Movie_farsi_name(self,Movie_farsi_name):

		Clear_screan()

		if Movie_farsi_name  == '':
			print('\nMovie farsi name need at least one letter.\n')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه هیچ نام فارسی ایی وارد نشده است\n')

			raise ValueError

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
				logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه نام فارسی فیلم نادرست وارد شده است\n')

				raise ValueError


		self.__class__.Movie[self.Movie_latin_name].append(Movie_farsi_name)

		self.Movie_farsi_name = Movie_farsi_name


	def Set_Show_times(self,times):

		Clear_screan()

		Start_time = times

		show_dict = {'1':"Morning_ShowTime",'2':"Afternoon_ShowTime",'3':"Night_ShowTime"}


		if times.count('') == 3:
			print('\nMovie need at least one show time.\n')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه هیچ زمان نمایشی برای فیلم در نظر گرفته نشده است\n')

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

		Clear_screan()

		if Start_time != '':
			try:
				Time = datetime.strptime(Start_time,"%H:%M")
				Time = Time.time()
				return Time

			except (ValueError , AttributeError):
				print('\nIncorrect start time')
				logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه زمان پخش فیلم نادرست وارد شده است\n')



		else:
			Time = ''
			return  Time


	def Set_Capacity(self,capacity):

		Clear_screan()

		if  capacity.isdigit() and  0 < int(capacity) <= 400:

			self.Capacity = capacity
		else:
			print('\nInvalid Capacity\n')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه ظرفیت سالن سینما نادرست وارد شده است\n')

			raise ValueError




	def Set_Days_num_of_week(self,Days_num_of_week):

		Clear_screan()

		Days_num_of_week  = Days_num_of_week .split(',')

		Capacity = self.Capacity

		days = []
		days_and_capacity = {}
		celender = {"0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday", "4": "Friday", "5": "Saturday", "6": "Sunday"}

		keys = self.__class__.Show_times.keys()


		for i in Days_num_of_week :
			if i.isdigit() and i != ',' and 0 <= int(i) <=6:
				day = celender[i]
				days_and_capacity[day] = int(Capacity)
				days.append(int(i))

			elif i == ',':
				continue

			else:
				print('\nInvalid days number')
				logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه روز های پخش فیلم نادرست وارد شده است\n')

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

		Clear_screan()

		genre_list = ['جنایی', 'اجتماعی/درام', 'اکشن/کمدی', 'ترسناک', 'ترسناک/رازآلود',
					  'تاریخی/درام/عاشقانه', 'خانوادگی/درام', 'کمدی']


		if genre in genre_list:
			self.Genre = genre

			self.__class__.Movie[self.Movie_latin_name].append(genre)

		else:
			print('\nInvalid genre')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه ژانر فیلم نادرست وارد شده است\n')

			raise ValueError



	def Set_Price(self,price):

		Clear_screan()

		if price.isdigit() and int(price) > 0:
			self.Price = price
			self.__class__.Movie[self.Movie_latin_name].append(int(price))

		else:
			print('\nInvalid Price')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه قیمت بلیط فیلم نادرست وارد شده است\n')

			raise ValueError

	def Set_Permissible_age(self,age):

		Clear_screan()

		if age.isdigit() and 0 <= int(age) < 41:
			self.Permissible_age = age
			self.__class__.Movie[self.Movie_latin_name].append(int(age))
			self.__class__.Movie[self.Movie_latin_name].append(int(self.Capacity))


			print('\nMovie added.\n')
			logging.info(f'فیلم با موفقیت اضافه شد.\n')

			Nosql_database.Add_Movie(self.__class__.Movie)

			self.__class__.Movie = {}


		else:
			print('\nInvalid Age')
			logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه سن مجاز تماشای فیلم نادرست وارد شده است\n')

			raise ValueError




	@classmethod
	def Add_Movie(cls):

		logging.info('دریافت اطلاعات مورد نیاز فیلم از ادمین برای وارد کردن فیلم در سایت.\n')

		Clear_screan()

		times =[]

		Movie_latin_name = input('\nEnter the Latin name of the movie:\n')

		Movie_farsi_name = input('\nEnter the Farsi name of the movie:\n')


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




		Days_num_of_week = input('\nEnter the number of days of the week on which the movie will be played:\n'
								 '\n\n-------------'
							     '\nExample:\n'
							     '\n6, 3, 2, 0\n'
							     '\nNumber of days of the week:\n'
							     '\nMonday: 0, Tuesday: 1, Wednesday: 2, Thursday: 3, Friday: 4,\n'
							     '\nSaturday: 5, Sunday: 6\n'
								 '\n--------------\n')



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

			except (ValueError , AttributeError):

				cls.Movie = {}

				print('\nTry again')
				break


