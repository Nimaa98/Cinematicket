

from abc import ABC
import re , os , logging
from noSQL_Database import Nosql_database




def Clear_screan() -> None:
    ''' Clears the screen'''

    os.system('clear')


class Bank(ABC):
    user_accounts = {}

    def __init__(self,cart_number:str,name:str,cvv2:str,password:str,balance:int):
        ''' five main attributes are defined in this function'''


        self.name , self._balance = name,balance
        self.cart_number, self.cvv2 = cart_number,cvv2
        self.__password = password


    def set_Cart_number(self,cart_number:str) -> None:
        ''' only valid cart number are allowed to set'''

        Clear_screan()

        result , name , other_Username,other_user_data = Nosql_database.Check_cart_numbers(cart_number)

        if ((re.match(r'^(\d{4}-){3}\d{4}|\d{16}$',cart_number)) and result
                and cart_number.count('-') == 3):

            self.cart_number= cart_number

        else:
            print('Cart Number is Wrong  or used by another user.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن کارت بانکی نادرست\n')

            raise ValueError


    def Cart_number(self) -> str:
        return self.cart_number



    def set_CVV2(self, cvv2:str) -> None:
        ''' only valid CVV2 are allowed to set'''

        Clear_screan()

        if len(cvv2) in (3,4) and cvv2.isdigit():
            self.cvv2 = cvv2
        else:
            print('Wrong CVV2\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن CVV2 نادرست\n')
            raise ValueError


    def CVV2(self) -> str:
        return self.cvv2


    def set_Password(self, password:str) -> None:
        ''' only valid password are allowed to set'''

        Clear_screan()

        if 3 < len(password) < 9 and password.isdigit():
            self.__password = password

        else:
            print('invalid password\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن پسورد نادرست\n')
            raise ValueError

    def Password(self) -> str:
        return self.__password



    def set_Owner_name(self, owner_name:str) -> None:
        ''' only valid owner name are allowed to set'''

        Clear_screan()

        if len(owner_name) > 1 and owner_name.isalpha():
            self.owner_name = owner_name

        else:
            print('invalid name\n')
            logging.warning('عدم اجرای درخواست کاربر به دلیل اینکه نام صاحب حساب اشتباه وارد شده است.\n')
            raise ValueError

    def Owner_name(self) -> str:
        return self.owner_name



class Bank_accounts(Bank):

    user_accounts = {}
    Minmum = 10_000
    Transaction_fees = 600


    def __init__(self,cart_number:str,name:str,cvv2:str,password:str,balance:int):
        ''' it inherits the five main attributes from the parent class'''

        super().__init__(cart_number,name,cvv2,password,balance)




    @classmethod
    def Add_amount(cls,Username:slice,user_data:dict,cart_number:slice,cart_info:dict,amount:int) -> None:
        '''Add balance to user account'''

        Clear_screan()

        balance = cart_info[3]
        balance += amount

        user_data[Username][6][cart_number][3] = balance
        Nosql_database.Add(user_data)

        print(f'The transaction was completed successfully.\n')
        logging.info('انجام موفقیت آمیز تراکنش .\n')


    @classmethod
    def Sub_amount(cls, Username:slice, user_data:dict, cart_number:slice, cart_info:dict, amount:int) -> int| None:
        '''Balance deduction from user account'''

        Clear_screan()

        print(f'account owner name: {cart_info[0]}\n')
        cvv2 = input('Enter cart cvv2:\n')
        password = input('Enter your password:\n')


        balance = cart_info[3]
        if balance - (amount + cls.Transaction_fees) < cls.Minmum:
            print('Not enough balance.\n')
            logging.warning('عدم اجرای درخواست کاربر به دلیل عدم موجودی کافی.\n')

            raise ValueError

        if cvv2 == cart_info[1] and password == cart_info[2]:

            balance -= amount + cls.Transaction_fees

            print('\nThe transaction was completed successfully.\n')
            logging.info('انجام موفقیت آمیز تراکنش .\n')

            user_data[Username][6][cart_number][3] = balance
            Nosql_database.Add(user_data)
            return amount

        else:
            print('\ncvv2 or password is incorrect.\ntry again later.\n')
            logging.warning('عدم اجرای درخواست کاربر به دلیل اینکه password یا CVV2 اشتباه وارد شده است.\n')

            raise ValueError




    @classmethod
    def Transfer(cls,Username:slice, user_data:dict, cart_number:slice, cart_info:dict, amount:int,cart_dest_number:str) -> None:
        '''Checking the information received from the user and the possibility of transferring money'''

        Clear_screan()

        if cart_number == cart_dest_number:
            print('\ncart number and cart dest number are the same.\n')
            logging.warning('عدم اجرای درخواست کاربر به دلیل یکسان بودن کارت مبدا و مقصد.\n')

            raise ValueError

        balance = cart_info[3]
        if balance - (amount + cls.Transaction_fees) < cls.Minmum:
            print('Not enough balance.\n')
            logging.warning('عدم اجرای درخواست کاربر به دلیل عدم موجودی کافی.\n')

            raise ValueError

        result, name , other_Username,other_user_data = Nosql_database.Check_cart_numbers(cart_dest_number)

        print(f'account owner name: {cart_info[0]}\n')

        print(f'Name of destination cart owner: {name}\n')

        cvv2 = input('Enter cart cvv2:\n')
        password = input('Enter your password:\n')

        if not result and cvv2 == cart_info[1] and password == cart_info[2]:

            Bank_accounts.Transfer_result(Username, user_data, cart_number, amount,cart_dest_number,
                                          other_Username,other_user_data)

        else:
            print('cart number not found or wrong cvv2/password.\n')
            logging.warning('عدم اجرای درخواست کاربر به دلیل اینکه password یا CVV2 یا شماره کارت اشتباه وارد شده است.\n')






    @classmethod
    def Transfer_result(cls,Username:slice, user_data:dict, cart_number:slice, amount:int,cart_dest_number:str,other_Username:slice,other_user_data:dict) -> None:
        '''Transfer money from the source account to the destination account'''

        Clear_screan()

        balance = user_data[Username][6][cart_number][3]
        other_balance = other_user_data[other_Username][6][cart_dest_number][3]

        if Username != other_Username:
            balance -= amount + cls.Transaction_fees
            user_data[Username][6][cart_number][3] = balance

            other_balance += amount
            other_user_data[other_Username][6][cart_dest_number][3] = other_balance


            user_data = user_data | other_user_data

            Nosql_database.Add(user_data)

        else:
            balance -= amount + cls.Transaction_fees
            other_balance += amount


            user_data[Username][6][cart_number][3] = balance
            user_data[Username][6][cart_dest_number][3] = other_balance

            Nosql_database.Add(user_data)

        print('successfully transferd.\n')
        logging.info('انجام موفقیت آمیز تراکنش .\n')





    @staticmethod
    def Manage_accounts(Username:str,user_data:dict) -> None:
        ''' it allows the user to choose between Adding bank account,View accounts and balance changing'''

        Clear_screan()

        while True:

            a = input('\npress 1 to Add bank account\n2 to see your accounts\n3 to change your balance\n0 to exit\n')

            if a == '1':
                try:
                    logging.info(f'اقدام کاربر برای اضافه کردن حساب بانکی.\n')
                    Bank_accounts.Add_account(Username, user_data)


                except ValueError:
                    print('try again')

            elif a == '2':
                logging.info(f'مشاهده حساب های بانکی.\n')

                Bank_accounts.Show_accounts(Username,user_data)

            elif a == '3':
                logging.info(f'اقدام کاربر برای تغییر موجودی حساب بانکی.\n')

                Bank_accounts.Show_accounts(Username, user_data)
                cart_number , cart_info = Change_Balance.Select_cart(Username,user_data)

                if cart_number != None:

                    Change_Balance.Manage_Balance(Username, user_data, cart_number, cart_info)


            elif a == '0':
                logging.info(f'خروج کاربر از بخش حساب های بانکی .\n')
                Clear_screan()
                break

            else:
                print('incorrect input try again')
                Clear_screan()



    @classmethod
    def Add_account(cls,Username:str,user_data:dict) -> None:
        '''Adding new bank account'''

        Clear_screan()

        print('\nThe right pattern of cart number is: aaaa-bbbb-cccc-dddd',
              'Example:3598-4322-9976-0912',sep ='\n')
        cart_number = input('Enter your cart number:\n')
        name = input('Enter  accounts owner name:\n')
        cvv2 = input('Enter cart cvv2:\n')
        password = input('Enter your password:\n')
        balance = 10_000

        inctance = cls(name,balance,cart_number,cvv2,password)

        inctance.set_Cart_number(cart_number)
        inctance.set_Owner_name(name)
        inctance.set_CVV2(cvv2)
        inctance.set_Password(password)


        user_data[Username][6][cart_number] = [name,cvv2,password,balance]

        Nosql_database.Add(user_data)


        print(f'\nyour cart number added.\n')
        logging.info(f'کارت بانکی جدید اضافه شد.\n')




    @classmethod
    def Show_accounts(cls,Username:str,user_data:dict) -> None:
        '''View current accounts'''

        Clear_screan()

        if len(user_data[Username][6]) == 0:

            a= input('\nyou dont have any bank account.\ndo you want make your first account?(yes/no)\n')

            if a == 'yes' or a =='YES':
                try:
                    logging.info(f'  عدم مشاهده ی حساب های بانکی بدلیل اینکه هنوز شماره کارتی وارد نشده است ---> هدایت کاربر به بخش وارد کردن حساب بانکی.\n')

                    Bank_accounts.Add_account(Username,user_data)

                except ValueError:
                    print('try again')

            elif a == 'no':

                logging.info(
                    f'  عدم مشاهده ی حساب های بانکی بدلیل اینکه هنوز شماره کارتی وارد نشده است ---> عدم تمایل کاربر به وارد کردن حساب بانکی جدید.\n')

                Bank_accounts.Manage_accounts(Username,user_data)
                print('\n')

            else:
                print('incorrect input\n')
                Bank_accounts.Manage_accounts(Username, user_data)

        else:
            print('\nThese are your accounts:\n')

        user_accounts = user_data[Username][6]

        i=1
        for cart in user_accounts:

            print(f'\naccount number {i}:\n Cart number: {cart}\n Owner account name: {user_accounts[cart][0]}\n'
                  f' CVV2: {user_accounts[cart][1]}\n'
                  ,50 * '*')
            i += 1


class Change_Balance(Bank_accounts):

    @staticmethod
    def Select_cart(Username:str,user_data:dict) -> tuple[str,str] | tuple[None,None]:
        '''Select a bank card to make the transaction'''

        Clear_screan()

        a = ''
        user_accounts = user_data[Username][6]

        if len(user_data[Username][6]) != 0:
            a = input('\nEnter the account number with which you want to make a transaction or charge wallet:\n')

        if a.isdigit() and 0 < int(a) <= len(user_accounts):

            logging.info(f'انتخاب کارت بانکی توسط کاربر.\n')


            a = int(a)
            a -=1
            list_of_carts = list(user_accounts)

            chosen_cart = list_of_carts[a]

            cart_info = user_accounts[chosen_cart]

            cart_number = chosen_cart

            return cart_number , cart_info

        print('No card was selected.\n')
        logging.warning(f'عدم انتخاب کارت بانکی توسط کاربر.\n')

        return None , None



    @staticmethod
    def Check_digit(amount:str) -> (bool,int):
        '''The amount entered for the transaction must be an integer'''

        Clear_screan()


        if amount.isdigit() and int(amount) >= 10000:

            amount = int(amount)
            return True ,amount

        print(f'\n{amount} is a invalid amount\n')
        logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد کردن مبلغ نادرست\n')

        return False , amount


    @staticmethod
    def Manage_Balance(Username:slice,user_data:dict,cart_number:slice,cart_info:dict) -> None:
        ''' it allows the user to change his balance by add ,sub and transfer options'''

        Clear_screan()

        while True:
            a = input('Select the transaction type:\n'
                      '1 for add balance\n2 for sub balance\n'
                      '3 for transfer money\n0 for exit\n')


            if a == '1':

                logging.info(f'تصمیم کاربر به افزایش موجودی.\n')

                print(f'account owner name: {cart_info[0]}\n')

                amount = input('Enter the amount you want to deposit into the account:\n')

                result , amount = Change_Balance.Check_digit(amount)

                if result:

                    Bank_accounts.Add_amount(Username,user_data,cart_number,cart_info,amount)

            elif a == '2':

                logging.info(f'تصمیم کاربر به کاهش موجودی.\n')

                amount = input('Enter the amount you want to withdraw from the account:\n')

                result, amount = Change_Balance.Check_digit(amount)

                if result:
                    try:
                        Bank_accounts.Sub_amount(Username, user_data, cart_number, cart_info, amount)
                    except ValueError:
                        print('try again later\n')


            elif a == '3':

                logging.info(f'تصمیم کاربر به انتقال وجه.\n')

                amount = input('Enter the amount you want to transfer:\n')

                cart_dest_number = input('Enter the destination card number:\n')

                result, amount = Change_Balance.Check_digit(amount)

                if result:
                    try:
                        Bank_accounts.Transfer(Username, user_data, cart_number, cart_info, amount,cart_dest_number)
                    except ValueError:
                        print('try again later\n')


            elif a =='0':
                logging.info(f'انصراف کاربر از تراکنش بانکی.\n')
                break


            else:
                print('incorrect input')


