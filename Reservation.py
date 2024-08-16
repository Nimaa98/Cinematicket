from datetime import datetime , timedelta , time
from noSQL_Database import Nosql_database
from bank_acounts import Bank_accounts , Change_Balance , Clear_screan
import math , logging


class Movies():
    now = datetime.now()
    Movies_dict = Nosql_database.Movies_info()
    days = []

    Username , user_data , wallet_id = None , None , None
    show_times = {"morning": "Morning_ShowTime", "afternoon": "Afternoon_ShowTime", "night": "Night_ShowTime"}




    def __init__(self,movie,day,show_time):
        self.movie = movie
        self.day = day
        self.show_time = show_time





    def show_time_setter(self,show_time,day):

        Clear_screan()

        today = self.__class__.now.strftime('%A')

        minute = self.Movies_dict[self.movie][2][show_time][0][0]
        hour = self.Movies_dict[self.movie][2][show_time][0][1]
        start_time = time(minute, hour)

        situation = self.Movies_dict[self.movie][2][show_time][2]

        if situation == 'Active' and day == today and self.__class__.now.time() > start_time:

            print('\nThe time allowed to buy this ticket has expired.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد منقضی شدن زمان پخش فیلم\n')

            raise ValueError

        elif situation == 'Deactive':
            print('\nSelected movie will not be played at this hour.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه فیلم انتخاب شده در این ساعت پخش نمی شود\n')

            raise ValueError


        else:
            return start_time



    def day_setter(self,movie,day):

        Clear_screan()

        celender = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}
        day_number = celender[day]
        days = self.__class__.Movies_dict[movie][1]



        if day_number not in days:

            print(f'\nSelected Movie not play in {day}.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه فیلم انتخاب شده در روز درخواستی کاربر پخش نمی شود \n')

            raise ValueError



class Purchas(Movies):

    def __init__(self,movie,day,show_time):
        super().__init__(movie,day,show_time)


    @classmethod
    def Date_format(cls):

        birthday = cls.user_data[cls.Username][4]
        date_format1 = "%Y-%m-%d"
        birthday = datetime.strptime(birthday, date_format1)

        signup_date = cls.user_data[cls.Username][5]
        date_format2 = "%Y-%m-%d"
        signup_date = datetime.strptime(signup_date,date_format2)

        logging.info('دریافت تاریخ تولد و تاریخ ثبت نام کاربر از دیتابیس و ارسال آنها به توابع مربوطه')

        return birthday , signup_date


    @classmethod
    def Choose(cls,Username,user_data):

        cls.Username = Username
        cls.user_data = user_data
        cls.wallet_id = user_data[Username][2]

        cls.Movies_dict = Nosql_database.Get_Movies()

        Clear_screan()

        while True:
            b = input('\npress 1 to see Cinema Program\n'
                      '2 to buy Cinema Ticket\n'
                      '0 to exit\n')

            if b == '1':

                logging.info(f'اقدام کاربر برای مشاهده لیست فیلم ها.\n')


                View_seat.Cinema_program(cls.Movies_dict)

            elif b == '2':

                logging.info(f'تصمیم کاربر برای انتخاب فیلم.\n')

                Purchas.Select()

            elif b == '0':
                logging.info(f'خروج از بخش رزرو فیلم.\n')
                Clear_screan()

                break

            else:
                print('\nIncorrect Input.\n')
                Clear_screan()


    @classmethod
    def Select(cls):

        Clear_screan()

        Movies = Nosql_database.Get_Movies()

        Movies = list(Movies.keys())

        Movies.remove('Movie name')

        print(f'\nThese are Cinema Ticket Movies:\n')

        for i in range(0, len(Movies), 3):
            chunk = Movies[i:i + 3]

            print(*chunk, sep='          ', end='\n')


        movie = input('\nWhich movie are you going to watch?\n(Use English letters)\n')

        day = input('\non which day do you plan to watch the movie??\n(Example: Friday)\n')

        show_time = input('\non Which show time do you plan to watch the movie?\n(Examples: morning,afternoon,night)\n')


        try:

            show_time = cls.show_times[show_time]

            instance = cls(movie, day, show_time)

            instance.day_setter(movie,day)
            start_time = instance.show_time_setter(show_time,day)

            logging.info(f'مشخص کردن نام و روز و ساعت پخش فیلم توسط کاربر.\n')

            print(f'\nInformation of the selected movie are:\n\n'
                  f'movie name: {cls.Movies_dict[movie][0]}\n'
                  f'show day: {day}\n'
                  f'show start time: {start_time}\n'
                  f'movie genre: {cls.Movies_dict[movie][3]}\n'
                  f'Capacity: {cls.Movies_dict[movie][2][show_time][1][day]}\n'
                  f'Ticket price: {cls.Movies_dict[movie][4]}\n')

            Purchas.Limit(movie,show_time,day)


        except (ValueError , KeyError):
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن اطلاعات اشتباه(نام فیلم یا روز و ساعت پخش فیلم) توسط کاربر\n')

            print('Try again\n')


    @classmethod
    def Limit(cls,movie,show_time,day):

        Clear_screan()

        birthday, signup_date = Purchas.Date_format()

        if cls.Movies_dict[movie][2][show_time][1][day] == 0:
            print('\nThe capacity is full\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل تکمیل بودن ظرفیت سینما در سانس درخواست شده\n')



        elif cls.Movies_dict[movie][5] > (cls.now.year - birthday.year):
            print('\nWatching this movie is not recommended for people under 18 years of age.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل اینکه سن کاربر برای مشاهده فیلم درخواستی مجاز نمی باشد\n')



        else:
            logging.info(f'ارسال اطلاعات مشخص شده توسط کاربر به تابع محاسبه تخفیف.\n')
            price = Purchas.Apply_discount(cls.Movies_dict[movie][4])

            logging.info(f'ارسال اطلاعات مشخص شده توسط کاربر به تابع خربد فیلم.\n')
            Purchas.Buy(movie, day, show_time, cls.Movies_dict[movie][2][show_time][1][day], price)




    @classmethod
    def Apply_discount(cls,price):

        Clear_screan()

        sub_discount = {'Bronze':0,'Silver':.2,'Golden':.5}

        birthday , signup_date = Purchas.Date_format()

        days = cls.now.date() - signup_date.date()
        month = math.floor(days.days/30)



        price = (1-sub_discount[cls.user_data[cls.Username][7][cls.wallet_id][0]]) * price

        if month <= 12:

            price = (1-(.01 * month)) * price

        else:

            price = (1 - .12) * price


        if cls.now.date().month == birthday.month and cls.now.date().day == birthday.day:

            price = (1 - .5) * price
            print('\nHappy Birthday'
                  '\nCinema Ticket gift to you is a 50% discount on your birthday\n')

        logging.info(f'اعمال تخفیف های مورد نظر روی قیمت اصلی فیلم.\n')

        return price


    @classmethod
    def Buy(cls,movie,day,show_time,capacity,price):

        Clear_screan()

        amount = price
        wallet_id = cls.user_data[cls.Username][2]

        a = input('\nHow do you pay?'
                  '\nif you want use your wallet press 1'
                  '\nor press 2 to use your bank account:\n')


        if a == '1':

            logging.info(f'تصمیم کاربر به خرید فیلم با استفاده از کیف پول.\n')

            balance = cls.user_data[cls.Username][7][wallet_id][2]

            if balance >= amount:
                balance -= amount
                cls.user_data[cls.Username][7][wallet_id][2] = balance

                print('\nSeat Reservation was successful.\n')
                capacity -= 1

                cls.Movies_dict[movie][2][show_time][1][day] = capacity

                Nosql_database.Add(cls.user_data)
                Nosql_database.Update_Movies(cls.Movies_dict)

                logging.info(f'خرید موفقیت آمیز فیلم.\n')


            else:
                print('not enough balance.\nplease charge your wallet first.\n')
                logging.warning('.عدم اجرای درخواست کاربر به دلیل موجودی ناکافی کیف پول\n')



        elif a == '2':

            logging.info(f'تصمیم کاربر به خرید فیلم با استفاده از حساب بانکی.\n')


            try:
                Bank_accounts.Show_accounts(cls.Username,cls.user_data)
                cart_number , cart_info = Change_Balance.Select_cart(cls.Username,cls.user_data)


                Bank_accounts.Sub_amount(cls.Username, cls.user_data, cart_number, cart_info, amount)

                capacity -= 1

                cls.Movies_dict[movie][2][show_time][1][day] = capacity

                print('\nSeat Reservation was successful.\n')
                Nosql_database.Update_Movies(cls.Movies_dict)

                logging.info(f'خرید موفقیت آمیز فیلم.\n')



            except (ValueError , TypeError):
                print('\ntry again later\n')


        else:
            print('\nIncorrect input')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن اطلاعات اشتباه توسط کاربر\n')






class View_seat(Movies):


    key = []
    new_Movie_dict ={}


    morning_start, afternoon_start, night_start = None, None, None

    @classmethod
    def Calc_date_range(cls):
        today = datetime.now()

        further_date = today + timedelta(days=6)

        date_range = [today + timedelta(days=i) for i in range((further_date - today).days + 1)]

        return  date_range


    @classmethod
    def Cinema_program(cls,Movies_dict):

        Clear_screan()

        flag = True


        print('\nMovies list:',60 * '-',sep='\n')

        date_range = View_seat.Calc_date_range()


        for i in date_range:


            print(i,i.strftime('%A'),i.weekday(),sep='   ')
            print('Cinema', i.strftime('%A'), 'Program:\n')

            for movie in Movies_dict:

                 if flag and i.weekday() in Movies_dict[movie][1] :
                    cls.key.append(movie)
                    View_seat.Show_Time(cls.key,Movies_dict,cls.now)


                 elif i.weekday() in Movies_dict[movie][1]:

                     cls.key = []
                     day = i.strftime('%A')

                     print(f'\nMovie name: {movie}\n'
                           f'Movie farsi name: {Movies_dict[movie][0]}\n'
                           f'Movie genre: {Movies_dict[movie][3]}\n'
                           f'Ticket Price: {Movies_dict[movie][4]}\n'
                           f'Show Times:')


                     show_times = Movies_dict[movie][2]
                     for j in show_times:

                        situation = Movies_dict[movie][2][j][2]
                        start_time = time(*Movies_dict[movie][2][j][0])
                        if situation == 'Active':

                            print(f'Start at: {start_time} ==> Remain Capacity: {Movies_dict[movie][2][j][1][day]}')
                            print(20*'-')

            print(70 * '*')

            flag = False


        logging.info(f'ارسال موفقیت آمیز برنامه هفتگی سینما از دیتابیس.\n')




    @classmethod
    def Show_Time(cls,key,Movies_dict,now):

        #Clear_screan()

        day = now.strftime('%A')
        now = now.time()
        cls.flag = True


        for movie in Movies_dict:
            if movie in key:
                cls.new_Movie_dict = {movie:Movies_dict[movie]}


        for movie in cls.new_Movie_dict:

            night_start = time(*Movies_dict[movie][2]["Night_ShowTime"][0])
            start_times = []


            print(f'\nMovie name: {movie}\n'
                  f'Movie farsi name: {cls.new_Movie_dict[movie][0]}\n'
                  f'Movie genre: {cls.new_Movie_dict[movie][3]}\n'
                  f'Ticket Price: {cls.new_Movie_dict[movie][4]}\n'
                  f'Show Times:\n')

            show_times = cls.new_Movie_dict[movie][2]

            n = 0
            for i in show_times:

                situation = cls.new_Movie_dict[movie][2][i][2]

                start_time = time(*Movies_dict[movie][2][i][0])
                start_times.append(start_time)

                if situation == 'Active' and now < start_time:

                    print(f'Start at: {start_time} ==> Remain Capacity: {cls.new_Movie_dict[movie][2][i][1][day]}')
                    print(20*'-')



                n += 1


            View_seat.Auto_Change_capacity(Movies_dict,movie,start_times,day,now)





    @classmethod
    def Auto_Change_capacity(cls,Movies_dict,movie,start_times,day,now):


        if  max(start_times) < now :

            print(f'there is no show time at now\n\n')

            Movies_dict[movie][2]["Morning_ShowTime"][1][day] = Movies_dict[movie][6]
            Movies_dict[movie][2]["Afternoon_ShowTime"][1][day] = Movies_dict[movie][6]
            Movies_dict[movie][2]["Night_ShowTime"][1][day] = Movies_dict[movie][6]

            Nosql_database.Update_Movies(Movies_dict)

            logging.info(f'آپدیت کردن ظرفیت فیلم پس از پایان روز.\n')






