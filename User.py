
import re,getpass,hashlib,uuid
from noSQL_Database import Nosql_database
from Subscription import Wallet , Manage
from Reservation import Purchas
from Separator import User_role
from Admin import Admin_application


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
        result, user_data = Nosql_database.Check(Username)

        if len(Username) == 0 or Username.isdigit():
            print('username must have at least 1 letter\n')
            raise ValueError


        self.names.append(Username)
        if self.names.count(Username) == 2 or result:
            print('the entered name is duplicate or has been selected by another user.\n')
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

    def new_password(self,user_data,Username):
        ''' remove old passwords and set new passwords'''
        old_Username = Username

        old_password = getpass.getpass('Enter the current password:')
        new_password_1 = getpass.getpass('Enter new password:')
        new_password_2 = getpass.getpass('Enter new password again:')
        if old_password != self.__password:
            print('incorrect password')

        elif old_password == new_password_1:
            print('the entered password is duplicate.\n')

        elif new_password_1 != new_password_2:
            print('the entered passwords do not match.\n')
        else:
            new_password = new_password_1
            self.__password = new_password
            hash_password = self.hash_password(new_password)

            user_data[Username][1] = new_password
            user_data[Username][3] = hash_password
            print('your password changed.\n')

            Nosql_database.Edit_data(user_data, old_Username, Username)





class User_Application(User):
    ''' using the condetions set in the parent class , it creats instance and changes it if needed'''
    user_data ={}

    def __init__(self,Username:str,phone_number:str ,password:str,iid:str):
        ''' it inherits the four main attributes from the parent class'''
        super().__init__(Username,phone_number ,password,iid)

    @classmethod
    def sign_up(cls):
        ''' registers new users'''

        Username = input('Enter your username:\n')
        
        flag = User_role.Check_user_role(Username)
        
        if flag:
            raise Exception

        phone_number = input('Enter your phone number:\n')
        password = getpass.getpass('Enter your password:\n')

        iid = uuid.uuid5(uuid.NAMESPACE_DNS,Username)

        instance = cls(Username,phone_number,password,iid)

        instance.set_Username(Username)
        instance.set_phone_number(phone_number,Username)
        instance.set_password(password,Username)

        hash_password = cls.hash_password(password)

        iid , hash_password = str(iid) , str(hash_password)

        cls.users_info[Username] = [phone_number,password,iid,hash_password]

        return Username


    @classmethod
    def Login(cls):
        ''' if the correct information is enterd, the user will be allowed to enter the account'''


        Username = input('Enter your username to Login:\n')

        result ,cls.user_data = Nosql_database.Check(Username)

        flag , password = Nosql_database.Check_Admin_name(Username)


        if flag:

            Admin_application.Login(password)


        elif Username not in cls.users_info and not result:

            print('No user found with this name.\n')

        else:
            password = getpass.getpass('Enter your password:\n')
            if cls.hash_password(password) == cls.user_data[Username][3]:

                print('\nLogin was done successfully\n')

                phone_number , iid = cls.user_data[Username][0] , cls.user_data[Username][2]

                instance = cls(Username,phone_number,password,iid)

                instance.User_account()

            else:
                print('incorrect password.\n')

    def User_account(self):
        ''' it allows the user to choose between viewing information,editing and changing the password'''

        from Date import Date
        from bank_acounts import Bank_accounts

        Wallet.Auto_Change_subscription(self.Username,self.user_data)

        while True:
            b = input('press 1 to see your informations\n'
                      '2 to Edit your username\n'
                      '3 to change phone number\n'
                      '4 to change password\n'
                      '5 to manage your bank accounts\n'
                      '6 to manage your wallet and subscription\n'
                      '7 to see Movies and Reserve seat\n'
                      '0 to exit\n')

            if b == '1':
                self.__str__()

            elif b == '2':
                self.edit_Username(self.user_data,self.Username)
            elif b == '3':
                self.edit_Phone_number(self.user_data,self.Username,self.phone_number)

            elif b == '4':
                self.new_password(self.user_data,self.Username)

            elif b == '5':

                Bank_accounts.Manage_accounts(self.Username,self.user_data)

            elif b == '6':

                Manage.Manage_wallet(self.Username,self.user_data)

            elif b == '7':

                Purchas.Choose(self.Username,self.user_data)

            elif b == '0':
                print('you have logged out of your account\n')
                break

            else:
                print('incorrect input try again')


    def __str__(self):
        ''' it allows the user to viewing information'''

        print(
            f'username is: {self.Username} \nphone_number is: {self.phone_number}'
            f' \nuser id is: {self.iid} \nuser birthday is: {self.user_data[self.Username][4]}'
            f'\nThe date of Registration is: {self.user_data[self.Username][5]}\n')




    def edit_Username(self,user_data,Username):
        ''' it allows the user to editing profile'''
        #print(user_data)

        try:
            old_Username = Username
            Username = input('Enter your new username:')

            if Username != old_Username:
                self.set_Username(Username)
                print('your username has changed\n')

                user_data[Username] = user_data.pop(old_Username)
                Nosql_database.Edit_data(user_data,old_Username,Username)



            if User.names.count(old_Username) == 1:
                User.names.remove((old_Username))


        except ValueError:
            print('incorrect input\n')


    def edit_Phone_number(self,user_data,Username,phone_number):

        try:
            old_Username = Username
            old_phone_number = phone_number
            phone_number = input('Enter your new phone_number:')

            self.set_phone_number(phone_number, Username)
            if old_phone_number != phone_number:
                print('your phone number has changed')
                user_data[Username][0] = phone_number

            Nosql_database.Edit_data(user_data, old_Username, Username)


        except ValueError:
            print('incorrect input\n')





