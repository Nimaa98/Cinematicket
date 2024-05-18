
from User import User , User_Application
from Date import Date




while True:
    a = input('press 1 to register or 2 to Login or 0 to exit: ')
    if a == '1':
        try:
            User_Application.sign_up()

            Date.Birthday()
            print(Date.users_info)


        except ValueError:
            print('try again')

    elif a=='2':
        User_Application.Login()

    elif a=='0':
        print(User.users_info)
        break

    else:
        print('incorrect input try again')





