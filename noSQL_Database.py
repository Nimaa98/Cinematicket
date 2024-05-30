import json
class Nosql_database:
    data = {}
    repet = 'No'

    @classmethod
    def Add(cls,users_info):


        with open('users_info.json', 'r',encoding='utf-8') as file:
            cls.data = json.load(file)

        cls.data.update(users_info)

        with open('users_info.json','+w',encoding='utf-8') as f:
            json.dump(cls.data, f ,ensure_ascii=False, indent=4)

    @classmethod
    def Check(cls,Username):

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
    def Edit_data(user_data,old_Username,Username):

        with open('users_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            data.pop(old_Username)

            data[Username] = user_data[Username]

            print('data keys is: ',data.keys())

        with open('users_info.json', '+w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)










