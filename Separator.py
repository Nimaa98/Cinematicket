

from enum import Enum
from Admin import Admin_application
import logging
 
 
class User_role(Enum):


    Admin = 'Admin_CinemaTicket_'

    def __str__(self) ->str:
        '''Returns the specified expression for admin'''

        return self.value

    def Check_user_role(role) -> None:
        '''If the new admin wants to register, his name will be sent to the registration function'''

        Username = role

        Username = Username[:19]

        if Username == User_role.Admin.value:

            logging.info('.ثبت نام ادمین جدید\n')

            return Admin_application.Sign_up(role)







