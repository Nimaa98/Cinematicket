
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
    def Insert(users_info,Username):

        cursor_obj = con.cursor()
        postgres_insert_query = '''insert into public.user_informations
        (id,username,phone_number,password,password_hash,birthday,signup_date)
         values (%s,%s,%s,%s,%s,%s,%s)
         '''
        record_to_insert = (users_info[Username][2],Username,users_info[Username][0],users_info[Username][1]
                            ,users_info[Username][3],users_info[Username][4],users_info[Username][5])

        cursor_obj.execute(postgres_insert_query,record_to_insert)
        con.commit()
        #cursor_obj.close()
        #con.close()


    @staticmethod
    def Edit(new_value,Username,column_name):#case_of_change):


        cursor_obj = con.cursor()

        user_data = f'''
        update 
        public.user_informations
        set {column_name} = %s
        WHERE username = %s
        '''

        cursor_obj.execute(user_data,(new_value,Username))
        con.commit()
        #cursor_obj.close()
        #con.close()

#Pgadmin.Edit('ali','alii','username')

























# if case_of_change in user_data:
#
#
#     update_query = '''update user_informations
#     set username = %s
#     where id = %s
#     '''
#
#     username = case_of_change
#     id = user
#     cursor_obj.execute()
# else:
#     pass


# cursor_obj.execute('SELECT * from public.user_informations')
# result = cursor_obj.fetchall()
# print(result)

























