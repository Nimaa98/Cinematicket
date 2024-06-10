
import psycopg2


con = psycopg2.connect(
    database = 'CinemaTicket',
    user = 'postgres',
    password = 'Ni1377ma$',
    host = 'localhost',
    port = '5432'
)


class Pgadmin:
    @staticmethod
    def Insert(user_data,Username):

        cursor_obj = con.cursor()
        postgres_insert_query = '''insert into public.user_basic_informations
        (id,username,phone_number,password,password_hash,birthday,signup_date)
         values (%s,%s,%s,%s,%s,%s,%s)
         '''
        record_to_insert = (user_data[Username][2],Username,user_data[Username][0],user_data[Username][1]
                            ,user_data[Username][3],user_data[Username][4],user_data[Username][5])

        cursor_obj.execute(postgres_insert_query,record_to_insert)
        con.commit()
        #cursor_obj.close()
        #con.close()

        Pgadmin.Insert_wallet(user_data,Username)


    @staticmethod
    def Insert_bank_accounts(user_data,Username,cart_number,name,cvv2,password,balance):

        cursor_obj = con.cursor()
        postgres_insert_query = '''insert into public.bank_account
        (cart_number,owner_name,cvv2,password,balance,user_id)
        values (%s,%s,%s,%s,%s,%s)
        '''

        record_to_insert = (cart_number,name,cvv2,password,balance,user_data[Username][2])

        cursor_obj.execute(postgres_insert_query, record_to_insert)
        con.commit()






    @staticmethod
    def Insert_wallet(user_data,Username):

        wallet_id = user_data[Username][2]
        sub_type = user_data[Username][7][wallet_id][0]
        purchase_date = user_data[Username][7][wallet_id][1]
        balance = 0

        cursor_obj = con.cursor()
        postgres_insert_query = '''insert into public.wallet
            (wallet_id,subscription,purchase_date,balance)
            values (%s,%s,%s,%s)
            '''

        record_to_insert = (wallet_id,sub_type,purchase_date,balance)

        cursor_obj.execute(postgres_insert_query, record_to_insert)
        con.commit()








    @staticmethod
    def Edit(new_value,Username,column_name):

        cursor_obj = con.cursor()

        user_data = f'''
        update 
        public.user_basic_informations
        set {column_name} = %s
        WHERE username = %s
        '''


        cursor_obj.execute(user_data,(new_value,Username))
        con.commit()
        #cursor_obj.close()
        #con.close()



    @staticmethod
    def Edit_account_balance(new_value, cart_number, column_name):
        cursor_obj = con.cursor()

        user_data = f'''
                update 
                public.bank_account
                set {column_name} = %s
                WHERE cart_number = %s
                '''

        cursor_obj.execute(user_data, (new_value, cart_number))
        con.commit()




    @staticmethod
    def Edit_wallet(new_value, wallet_id, column_name):
        cursor_obj = con.cursor()

        user_data = f'''
                    update 
                    public.wallet
                    set {column_name} = %s
                    WHERE wallet_id = %s
                    '''

        cursor_obj.execute(user_data, (new_value, wallet_id))
        con.commit()


