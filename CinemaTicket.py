
from User import User , User_Application




while True:
    a = input('press 1 to register or 2 to Login or 0 to exit: ')
    if a == '1':
        try:
            User_Application.sign_up()
            print('Registration was successfull','\n')

        except ValueError:
            print('try again')

    elif a=='2':
        User_Application.Login()

    elif a=='0':
        print(User.users_info)
        break

    else:
        print('incorrect input try again')





