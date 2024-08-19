import json



class Nosql_database:
    data = {}
    repet = 'No'
    cart_numbers = []
    name = ''

    @classmethod
    def Add(cls,users_info:dict) -> None:
        ''' adding Users to database'''

        with open('users_info.json', 'r',encoding='utf-8') as file:
            cls.data = json.load(file)

        cls.data.update(users_info)

        with open('users_info.json','+w',encoding='utf-8') as f:
            json.dump(cls.data, f ,ensure_ascii=False, indent=4)

    @classmethod
    def Check(cls,Username:str)-> tuple[bool,dict]:
        '''Checks whether the name entered by the user is available in the
         database or not and if it is, return user information'''

        user_data = {}

        with open('users_info.json', 'r', encoding='utf-8') as f:
            Data = json.load(f)

            if Username in Data:
                cls.repet = 'Yes'
                user_data = {Username:Data[Username]}


        if cls.repet == 'Yes':
            cls.repet = 'No'
            return True , user_data
        return False , user_data



    @staticmethod
    def Edit_data(user_data:dict,old_Username:str,Username:str)-> None:
        '''After editing the information by the user, the new information is entered in the database'''

        with open('users_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            data.pop(old_Username)

            data[Username] = user_data[Username]

        with open('users_info.json', '+w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    @staticmethod
    def Check_cart_numbers(cart_number:str)-> tuple[bool,str,str,dict]:
        '''Checks whether the entered card number is available in the database or not'''

        name = ''
        other_Username = ''
        other_user_data = {}

        with open('users_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for i,j in data.items():

            key = j[6].keys()

            if cart_number in list(key):

                name = j[6][cart_number][0]
                other_Username = i
                other_user_data = {i:data[i]}

                return False , name , other_Username,other_user_data

        return True , name , other_Username,other_user_data


    @staticmethod
    def Accounts_info(Username:str)->None:
        '''imports user information from the database'''

        with open('users_info.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

            user_date = data[Username][6]
            return user_date





    @staticmethod
    def Movies_info():
        '''It returns the list of movies along with their information'''

        with open('Movies.json', 'r', encoding='utf-8') as f:
            Movies_dict = json.load(f)


            return Movies_dict



    @classmethod
    def Add_Admin(cls,Admin_info):
        '''Enters new admin information into the database'''

        with open('Admin_info.json', 'r',encoding='utf-8') as file:
            cls.data = json.load(file)

        cls.data.update(Admin_info)

        with open('Admin_info.json','+w',encoding='utf-8') as f:
            json.dump(cls.data, f ,ensure_ascii=False, indent=4)


    @classmethod
    def Check_Admin_name(cls,Username):
        '''It checks whether the admin name exists in the database or not'''

        with open('Admin_info.json', 'r',encoding='utf-8') as file:
            cls.data = json.load(file)

            if Username in cls.data:

                password = cls.data[Username]

                return True , password

            return False ,None

    @classmethod
    def Add_Movie(cls,Movie):
        '''Add the new movies to the database'''

        with open('Movies.json', 'r',encoding='utf-8') as file:
            cls.data = json.load(file)

        cls.data.update(Movie)

        with open('Movies.json','+w',encoding='utf-8') as f:
            json.dump(cls.data, f ,ensure_ascii=False, indent=4)



    @staticmethod
    def Update_Movies(Movies_dict:str)->None:
        '''Enter the capacity of the cinema in the database after the change.'''

        with open('Movies.json', '+w',encoding='utf-8') as f:
            json.dump(Movies_dict,f,ensure_ascii=False,indent=4)


    @classmethod
    def Delete_Movie(cls,Movie):
        '''delete the selected movie from database'''

        with open('Movies.json', 'r',encoding='utf-8') as file:
            cls.data = json.load(file)

        cls.data.pop(Movie)


        with open('Movies.json','+w',encoding='utf-8') as f:
            json.dump(cls.data, f ,ensure_ascii=False, indent=4)







