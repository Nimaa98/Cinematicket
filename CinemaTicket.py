
import logging
from User import User , User_Application , Clear_screan
from Date import Date
from Log_setting import Log_config





Log_config()
logging.info('شروع برنامه....\n\n')

while True:


     a = input('press 1 to register or 2 to Login or 0 to exit: ')

     Clear_screan()
             
     if a == '1':
          try:
              Username = User_Application.sign_up()
              Date.Birthday(Username)

          except ValueError:
               print('try again')
               
          except Exception:
                   pass

     elif a=='2':
         User_Application.Login()
           


     elif a=='0':
         logging.info('اتمام برنامه')
         break

     else:
         print('incorrect input try again')
            




