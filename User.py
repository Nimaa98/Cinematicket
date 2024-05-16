
import re,getpass,hashlib,uuid

class User:
    ''' the coorect conditions for receiving entry in this class are determined'''
    users_info = {}
    names = []

    def __init__(self,Username:str,phone_number:str ,password:str,iid:str):
        ''' four main attributes are defined in this function'''

        self.Username , self.phone_number  = Username , phone_number
        self.__password , self.iid = password , iid



    def set_Username(self,Username:str):
        ''' only valid names are allowed to register'''

        if len(Username) == 0:
            print('username must have at least 1 letter')
            raise ValueError

        self.names.append(Username)
        if self.names.count(Username) == 2:
            print('the entered name is duplicate or has been selected by another user')
            self.names.remove((Username))
            raise ValueError
        self.Username = Username

    def get_Username(self):
        return self.Username


    def set_phone_number(self,phone_number:str,Username:str):
        ''' only valid phone numbers are allowed to register '''

        if re.match(r'^09\d{9}$',phone_number) or phone_number == '' :
            self.phone_number = phone_number
        else:
            print('invalid phone number')
            self.names.remove((Username))
            raise ValueError

    def get_phone_number(self):
        return self.phone_number

    @staticmethod
    def hash_password(password:str):
        '''hashing password with sha256'''
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


    def set_password(self,password:str,Username:str):
        ''' only valid passwords are allowed to register '''

        if 3 < len(password)<9:
            self.__password = password

        else:
            print('invalid password')
            self.names.remove((Username))
            raise ValueError

    def get_password(self):
        return self.__password

    def new_password(self):
        ''' remove old passwords and set new passwords'''

        old_password = getpass.getpass('Enter the current password:')
        new_password_1 = getpass.getpass('Enter new password:')
        new_password_2 = getpass.getpass('Enter new password again:')
        if old_password != self.__password:
            print('incorrect password')

        elif old_password == new_password_1:
            print('the entered password is duplicate')

        elif new_password_1 != new_password_2:
            print('the entered passwords do not match')
        else:
            new_password = new_password_1
            self.__password = new_password
            hash_password = self.hash_password(new_password)
            self.change_password(new_password,self.users_info,self.Username,hash_password)




class User_Application(User):
    ''' using the condetions set in the parent class , it creats instance and changes it if needed'''

    def __init__(self,Username:str,phone_number:str ,password:str,iid:str):
        ''' it inherits the four main attributes from the parent class'''
        super().__init__(Username,phone_number ,password,iid)

    @classmethod
    def sign_up(cls):
        ''' registers new users'''

        Username = input('Enter your username:')
        phone_number = input('Enter your phone number:')
        password = getpass.getpass('Enter your password:')
        iid = uuid.uuid5(uuid.NAMESPACE_DNS,Username)

        instance = cls(Username,phone_number,password,iid)

        instance.set_Username(Username)
        instance.set_phone_number(phone_number,Username)
        instance.set_password(password,Username)

        hash_password = cls.hash_password(password)

        cls.users_info[Username] = [phone_number,password,iid,hash_password]


    @classmethod
    def Login(cls):
        ''' if the correct information is enterd, the user will be allowed to enter the account'''

        Username = input('Enter your username to Login:')
        if Username not in cls.users_info:
            print('No user found with this name')
        else:
            password = getpass.getpass('Enter your password:')
            if cls.hash_password(password) == cls.users_info[Username][3]:
                print('Login was done successfully')

                phone_number , iid = cls.users_info[Username][0] , cls.users_info[Username][2]

                instance = cls(Username,phone_number,password,iid)

                instance.User_account()

            else:
                print('incorrect password')


    def User_account(self):
        ''' it allows the user to choose between viewing information,editing and changing the password'''

        while True:
            b = input('press 1 to see your informations or 2 to Edit or 3 to change password or 4 to exit:')

            if b == '1':
                self.__str__()

            elif b == '2':
                self.edit_profile()

            elif b == '3':
                self.new_password()

            elif b == '4':
                print('you have logged out of your account')
                break

            else:
                print('incorrect input try again')


    def __str__(self):
        ''' it allows the user to viewing information'''
        print(
            f'username is: {self.Username} \nphone_number is: {self.phone_number} \nuser id is: {self.iid}')


    def edit_profile(self):
        ''' it allows the user to editing profile'''

        old_Username = self.Username
        old_phone_number = self.phone_number

        Username = input('Enter your new username:')
        phone_number = input('Enter your new phone_number:')
        try:
            if Username != old_Username:
                self.set_Username(Username)
                self.names.remove(old_Username)
                print('your username has changed')

            self.set_phone_number(phone_number,Username)
            if old_phone_number != phone_number:
                print('your phone number has changed')

            self.users_info[Username] = self.users_info.pop(old_Username)
            self.users_info[Username][0] = phone_number

        except ValueError:
            pass


    @staticmethod
    def change_password(new_password:str,users_info:dict,Username:str,hash_password):
        ''' set the new password as the user's password and the user
        is allowed to enter the account by entring this password '''

        users_info[Username][1] = new_password
        users_info[Username][3] = hash_password
        print('your password changed')

