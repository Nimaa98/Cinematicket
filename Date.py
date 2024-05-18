import re
from User import User,User_Application
from datetime import date


class Check_birthday:

    def set_birthday(self,birth_day,Username):
        
        if re.match(r'(19[0-9][0-9]|20[0-1][0-8])-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])',birth_day):
            self.birth_day = birth_day

            User.users_info[Username].append(birth_day)
            User.users_info[Username].append(date.today())

            print('Registration was successfull', '\n')

        elif birth_day == '0':
            Date.Check_users_info()

        else:
            print('Incorrect date!', '\n')
            Date.Birthday()

    def get_birthday(self):
        return self.birthday


class Date(Check_birthday):
    users_info = User.users_info

    def __init__(self,birth_day):
        self.birth_day = birth_day

    @classmethod
    def Birthday(cls):

        print('The right pattern of birthday is YYYY-MM-DD','Example:2000-01-15','maximum valid birthday is:2018-12-31',sep ='\n')
        birth_day = input('Enter your birthday or press 0 to exit: ')

        Username = User.names[len(User.names) - 1]

        instance = cls(birth_day)
        instance.set_birthday(birth_day,Username)


    @staticmethod
    def Check_users_info():

        User.users_info.popitem()
        User.names.pop()
        #print(User.users_info)
        #print(User.names)

    @classmethod
    def change_Birthday(cls,Username,birthday):
        old_birthday = birthday
        new_birthday = input('Enter your new birthday: ')

        if (old_birthday != new_birthday and
                re.match(r'(19[0-9][0-9]|20[0-1][0-8])-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])', new_birthday)):

            User.users_info[Username][4] = new_birthday
            print('your birthday changed\n')

        else:
            print('Try again\n')




