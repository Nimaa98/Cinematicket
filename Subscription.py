
from noSQL_Database import Nosql_database
from bank_acounts import Bank_accounts , Change_Balance , Clear_screan
from datetime import datetime , timedelta, date
import logging




class Wallet:

    subs_list = ['Bronze','Silver','Golden']
    wallet_id = None
    subs_prices = {'Bronze': 0,'Silver': 150000 , 'Golden': 250000}
    result = False


    @classmethod
    def wallet(cls,Username:str,user_data:dict)-> dict:
        '''Creating a wallet automatically by the program for the user'''

        cls.wallet_id = user_data[Username][2]
        signup_date = user_data[Username][5]


        wallet_dict = {cls.wallet_id : [cls.subs_list[0] , signup_date , 0]}
        user_data[Username].append(wallet_dict)

        logging.info(f'ساخت کیف پول به صورت خودکار توسط برنامه برای کاربر .\n')

        return user_data


    @staticmethod
    def Auto_Change_subscription(Username:str,user_data:dict)-> None:
        '''Expire user subscription after one month and set subscription to bronze level'''

        Clear_screan()

        wallet_id = user_data[Username][2]

        purchase_date = user_data[Username][7][wallet_id][1]


        purchase_date = datetime.strptime(purchase_date,'%Y-%m-%d')

        expiration_date = purchase_date + timedelta(days=30)
        expiration_date = expiration_date.strftime('%Y-%m-%d')

        today = datetime.now()
        today = today.strftime('%Y-%m-%d')

        if today > expiration_date:

            if user_data[Username][7][wallet_id][0] != 'Bronze':
                print('\nYour subscription has expired.\n')

            if user_data[Username][7][wallet_id][0] == 'Golden':
                drink_price = 50000
                balance = user_data[Username][7][wallet_id][2]
                balance += drink_price

                user_data[Username][7][wallet_id][2] = balance
                print('\nYou have used the golden subscription in the last month.'
                      '\nAs a bonus, the cost of an energy drink was added to your wallet.\n')


            user_data[Username][7][wallet_id][0] = 'Bronze'

            user_data[Username][7][wallet_id][1] =today

            Nosql_database.Add(user_data)

            logging.info(f'منقضی شدن اشتراک کاربر و تنظیم اشتراک در سطح برنزی.\n')




    @staticmethod
    def Take_cart_info(Username:str,user_data:dict)-> None| dict:
        '''Get the user's bank account information from the database'''

        Clear_screan()

        if len(user_data[Username][6]) == 0:
            print('\nyou dont have any bank account pleas make one from manage account.\n')

            logging.warning('.عدم اجرای درخواست کاربر به دلیل نداشتن حساب بانکی\n')



        else:

            Bank_accounts.Show_accounts(Username,user_data)
            cart_number , cart_info = Change_Balance.Select_cart(Username,user_data)

            return  cart_number, cart_info


class Manage(Wallet):


    @classmethod
    def Manage_wallet(cls,Username:str,user_data:dict) -> None:
        ''' it allows the user to choose between viewing wallet information,Increasing wallet balance and purchasing subscription'''
        Clear_screan()

        cls.wallet_id = user_data[Username][2]
        while True:

            a = input('\npress 1 for see your wallet informations\n'
                      '2 for Increase wallet balance\n3 for Buy subscription\n'
                      '0 to exit.\n')

            if a == '1':

                Manage.See_info(Username,user_data)

            elif a == '2':

                logging.info(f'اقدام کاربر برای افزایش موجودی کیف پول.\n')
                Manage.Recharg_wallet(Username,user_data)


            elif a =='3':

                logging.info(f'اقدام کاربر برای خرید اشتراک .\n')

                Manage.Explaination(Username,user_data)


            elif a == '0':
                logging.info(f'خروج کاربر از بخش اشتراک .\n')
                Clear_screan()
                break

            else:
                print('invalid input.')
                Clear_screan()




    @classmethod
    def See_info(cls,Username:str,user_data:dict) -> None:
        '''View subscription status and wallet balance'''

        Clear_screan()

        cls.wallet_id = user_data[Username][2]
        balance = user_data[Username][7][cls.wallet_id][2]
        sub_type = user_data[Username][7][cls.wallet_id][0]

        print(50 * '-',
              f'\nyour wallet balance is: {balance} Toman.\n'
              f'\nyour Subscription type is: {sub_type}.\n',
              50 * '-','\n')


        logging.info(f'مشاهده وضعیت اشتراک و موجودی کیف پول.\n')



    @classmethod
    def Recharg_wallet(cls,Username:str,user_data:dict)-> None:
        '''Increase wallet balance if possible'''

        Clear_screan()

        cart_number, cart_info = Wallet.Take_cart_info(Username,user_data)

        if cart_number != None:

            charge_amount = input('\nHow much do you charge your wallet?\n')

            cls.result , amount = Change_Balance.Check_digit(charge_amount)



        if cls.result:

            try:
                amount = Bank_accounts.Sub_amount(Username, user_data, cart_number, cart_info, amount)

                wallet_balance = user_data[Username][7][cls.wallet_id][2]

                wallet_balance += amount
                cls.result = False

                user_data[Username][7][cls.wallet_id][2] += amount
                Nosql_database.Add(user_data)

                logging.info(f'افزایش موجودی کیف پول.\n')



            except ValueError:
                print('\nThe operation was unsuccessful.\n')
                logging.warning('.عدم شارژ کیف پول\n')


    @classmethod
    def Explaination(cls,Username:str,user_data:dict)-> None:
        '''Viewing site subscription information and selecting the user's desired subscription'''

        Clear_screan()

        print(50 * '-',
            '\nSubscriptions:\n'
            '\nBronze: This service is simple and has no special privileges.  ==> free\n'
            '\nSilver: This service returns 20% of the amount of each transaction'
            'to your wallet for up to three subsequent purchases.  ==> 150,000 toman\n'
            '\nGolden: This service returns 50% of the amount of each transaction to your wallet until the following month.\n'
            'and You will also receive a free energy drink. ==> 250,000 toman\n',
              50 * '-')

        sub_type = user_data[Username][7][cls.wallet_id][0]

        print(f'this is your current Subscriptions: {sub_type}\n')

        next_sub = input('Which Subscription do you want to buy?\n')
        next_sub = next_sub.capitalize()


        if next_sub.capitalize() == sub_type:
            print('you already have this Subscription.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل فعال بودن اشتراک درخواستی\n')



        elif next_sub in cls.subs_list:
            Manage.Change_subscription(Username,user_data,next_sub)

        else:
            print('incorrect input.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل وارد نکردن نوع اشتراک \n')





    @classmethod
    def Change_subscription(cls,Username:str, user_data:dict,next_sub:str)-> None:
        '''Buy a subscription with a wallet or bank account'''

        Clear_screan()

        amount = cls.subs_prices[next_sub]

        a = input('\nyou have two options for purchasing a Subscription:\n'
                  'option number 1: wallet\n'
                  'option number 2: bank account\n'
                  'which one do you take?\n')

        if a == '1':

            logging.info(f'تصمیم کاربر به خرید اشتراک با کیف پول.\n')

            balance = user_data[Username][7][cls.wallet_id][2]

            if balance >= amount:
                balance -= amount
                user_data[Username][7][cls.wallet_id][2] = balance
                user_data[Username][7][cls.wallet_id][0] = next_sub

                Nosql_database.Add(user_data)
                print(f'\n{next_sub} Subscriptions activated for you.\n')

                purchase_date = str(date.today())
                user_data[Username][7][cls.wallet_id][1] = purchase_date

                logging.info(f'خرید اشتراک توسط کاربر.\n')


            else:
                print('not enough balance.\nplease charge your wallet first.\n')
                logging.warning('.عدم اجرای درخواست کاربر به دلیل عدم موجودی کافی در کیف پول\n')



        elif a =='2':

            logging.info(f'تصمیم کاربر به خرید اشتراک با حساب بانکی.\n')

            cart_number, cart_info = Wallet.Take_cart_info(Username, user_data)



            try:

                Bank_accounts.Sub_amount(Username, user_data,cart_number, cart_info,amount)

                user_data[Username][7][cls.wallet_id][0] = next_sub

                Nosql_database.Add(user_data)
                print(f'\n{next_sub} Subscriptions activated for you.\n')

                purchase_date = str(date.today())
                user_data[Username][7][cls.wallet_id][1] = purchase_date

                logging.info(f'خرید اشتراک توسط کاربر.\n')


            except (ValueError , TypeError):
                print('\nThe operation was unsuccessful.\n')
                logging.warning('.عدم اجرای درخواست کاربر به دلیل تراکنش ناموفق\n')


        else:
            print('incorrect input.\n')
            logging.warning('.عدم اجرای درخواست کاربر به دلیل مشخص نکردن روش پرداخت \n')








