

from abc import ABC
import re
from noSQL_Database import Nosql_database


class Bank(ABC):
    user_accounts = {}

    def __init__(self,cart_number,name,cvv2,password,balance):
        self.name , self._balance = name,balance
        self.cart_number, self.cvv2 = cart_number,cvv2
        self.__password = password


    def set_Cart_number(self,cart_number):

        result , name , other_Username,other_user_data = Nosql_database.Check_cart_numbers(cart_number)

        if ((re.match(r'^(\d{4}-){3}\d{4}|\d{16}$',cart_number)) and result
                and cart_number.count('-') == 3):

            self.cart_number= cart_number

        else:
            print('Cart Number is Wrong  or used by another user.\n')
            raise ValueError


    def Cart_number(self):
        return self.cart_number



    def set_CVV2(self, cvv2):

        if len(cvv2) in (3,4) and cvv2.isdigit():
            self.cvv2 = cvv2
        else:
            print('Wrong CVV2\n')
            raise ValueError


    def CVV2(self):
        return self.cvv2


    def set_Password(self, password):

        if 3 < len(password) < 9 and password.isdigit():
            self.__password = password

        else:
            print('invalid password\n')
            # self.user_accounts.popitem((cart_number))
            raise ValueError

    def Password(self):
        return self.__password



    def set_Owner_name(self, owner_name):

        if len(owner_name) > 1 and owner_name.isalpha():
            self.owner_name = owner_name

        else:
            print('invalid name\n')
            # self.user_accounts.popitem((cart_number))
            raise ValueError

    def Owner_name(self):
        return self.owner_name


class Bank_accounts(Bank):

    user_accounts = {}
    Minmum = 10_000
    Transaction_fees = 600


    def __init__(self,cart_number,name,cvv2,password,balance):
        super().__init__(cart_number,name,cvv2,password,balance)





    @classmethod
    def Add_amount(cls,Username,user_data,cart_number,cart_info,amount):


        balance = cart_info[3]
        balance += amount

        user_data[Username][6][cart_number][3] = balance
        Nosql_database.Add(user_data)

        print(f'The transaction was completed successfully.\n')





    @classmethod
    def Sub_amount(cls, Username, user_data, cart_number, cart_info, amount):

        print(f'account owner name: {cart_info[0]}\n')
        cvv2 = input('Enter cart cvv2:\n')
        password = input('Enter your password:\n')


        balance = cart_info[3]
        if balance - (amount + cls.Transaction_fees) < cls.Minmum:
            print('Not enough balance.\n')
            raise ValueError

        if cvv2 == cart_info[1] and password == cart_info[2]:

            balance -= amount + cls.Transaction_fees

            print('\nThe transaction was completed successfully.\n')
            user_data[Username][6][cart_number][3] = balance
            Nosql_database.Add(user_data)
            return amount
        else:
            print('\ncvv2 or password is incorrect.\ntry again later.\n')
            raise ValueError





    @classmethod
    def Transfer(cls,Username, user_data, cart_number, cart_info, amount,cart_dest_number):

        balance = cart_info[3]
        if balance - (amount + cls.Transaction_fees) < cls.Minmum:
            print('Not enough balance.\n')
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





    @classmethod
    def Transfer_result(cls,Username, user_data, cart_number, amount,cart_dest_number,other_Username,other_user_data):

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




    @staticmethod
    def Manage_accounts(Username,user_data):


        while True:
            a = input('\npress 1 to Add bank account\n2 to see your accounts\n3 to change your balance\n0 to exit\n')

            if a == '1':
                try:
                    Bank_accounts.Add_account(Username, user_data)

                except ValueError:
                    print('try again')

            elif a == '2':
                Bank_accounts.Show_accounts(Username,user_data)

            elif a == '3':

                Bank_accounts.Show_accounts(Username, user_data)
                cart_number , cart_info = Change_Balance.Select_cart(Username,user_data)

                if cart_number != None:

                    Change_Balance.Manage_Balance(Username, user_data, cart_number, cart_info)


            elif a == '0':
                break

            else:
                print('incorrect input try again')



    @classmethod
    def Add_account(cls,Username,user_data):

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



    @classmethod
    def Show_accounts(cls,Username,user_data):

        if len(user_data[Username][6]) == 0:

            a= input('\nyou dont have any bank account.\ndo you want make your first account?(yes/no)\n')

            if a == 'yes' or a =='YES':
                try:
                    Bank_accounts.Add_account(Username,user_data)

                except ValueError:
                    print('try again')

            elif a == 'no':
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
    def Select_cart(Username,user_data):

        a = ''
        user_accounts = user_data[Username][6]

        if len(user_data[Username][6]) != 0:
            a = input('\nEnter the account number with which you want to make a transaction or charge wallet:\n')


        if a.isdigit() and 0 < int(a) <= len(user_accounts):

            a = int(a)
            a -=1
            list_of_carts = list(user_accounts)

            chosen_cart = list_of_carts[a]

            cart_info = user_accounts[chosen_cart]

            cart_number = chosen_cart

            return cart_number , cart_info

        print('incorrect input.\n')

        return None , None


    @staticmethod
    def Check_digit(amount):


        if amount.isdigit() and int(amount) >= 10000:

            amount = int(amount)
            return True ,amount

        print(f'\n{amount} is a invalid amount\n')
        return False , amount


    @staticmethod
    def Manage_Balance(Username,user_data,cart_number,cart_info):

        while True:
            a = input('Select the transaction type:\n'
                      '1 for add balance\n2 for sub balance\n'
                      '3 for transfer money\n0 for exit\n')

            if a == '1':

                print(f'account owner name: {cart_info[0]}\n')

                amount = input('Enter the amount you want to deposit into the account:\n')

                result , amount = Change_Balance.Check_digit(amount)

                if result:

                    Bank_accounts.Add_amount(Username,user_data,cart_number,cart_info,amount)

            elif a == '2':
                amount = input('Enter the amount you want to withdraw from the account:\n')

                result, amount = Change_Balance.Check_digit(amount)

                if result:
                    try:
                        Bank_accounts.Sub_amount(Username, user_data, cart_number, cart_info, amount)
                    except ValueError:
                        print('try again later\n')


            elif a == '3':
                amount = input('Enter the amount you want to transfer:\n')

                cart_dest_number = input('Enter the destination card number:\n')

                result, amount = Change_Balance.Check_digit(amount)

                if result:
                    try:
                        Bank_accounts.Transfer(Username, user_data, cart_number, cart_info, amount,cart_dest_number)
                    except ValueError:
                        print('try again later\n')


            elif a =='0':
                break


            else:
                print('incorrect input')


