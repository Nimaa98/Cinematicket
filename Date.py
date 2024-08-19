import logging
import re
from noSQL_Database import Nosql_database
from User import User,User_Application , Clear_screan
from datetime import date
from Subscription import Wallet



class Check_birthday:
    bank_acounts = {}
    wallet = {}

    def set_birthday(self,birth_day:str,Username:str)->None:
        ''' only valid birthdays are allowed to register'''

        Clear_screan()

        if re.match(r'(19[0-9][0-9]|20[0-1][0-8])-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])',birth_day):
            self.birth_day = birth_day

            Check_birthday.Make_account(Username,birth_day)


        elif birth_day == '0':
            Date.Check_users_info()

        else:
            print('Incorrect date!', '\n')
            logging.warning('.عدم ثبت نام کاربر به دلیل وارد کردن تاریخ تولد نادرست\n')

            Date.Birthday(Username)



    def get_birthday(self):
        return self.birthday




    @classmethod
    def Make_account(cls,Username:str,birth_day:str)->None:
        '''Creating an account for the user'''

        Clear_screan()

        today = str(date.today())

        User.users_info[Username].append(birth_day)
        User.users_info[Username].append(today)
        User.users_info[Username].append(cls.bank_acounts)

        user_data = Wallet.wallet(Username,User.users_info)

        Nosql_database.Add(user_data)


        print('Registration was successfull', '\n')

        logging.info('ثبت نام کاربر جدیدبا موفقیت انجام شد.\n')



class Date(Check_birthday):
    users_info = User.users_info

    def __init__(self,birth_day:str):
        ''' one main attribute are defined in this function'''

        self.birth_day = birth_day



    @classmethod
    def Birthday(cls,Username:str)->None:
        '''Get the user's date of birth during registration'''

        Clear_screan()

        print('The right pattern of birthday is YYYY-MM-DD','Example:2000-01-15','maximum valid birthday is:2018-12-31',sep ='\n')
        birth_day = input('Enter your birthday or press 0 to exit: ')

        instance = cls(birth_day)

        instance.set_birthday(birth_day,Username)


    @staticmethod
    def Check_users_info()->None:
        '''Deleting user information from temporary memory due to completion of registration or failed registration'''

        User.users_info.popitem()
        User.names.pop()






