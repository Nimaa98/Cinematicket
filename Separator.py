

from enum import Enum
from Admin import Admin_application
import logging
 
 
class User_role(Enum):


    Admin = 'Admin_CinemaTicket_'

    def __str__(self):

        return self.value

    def Check_user_role(role):

        Username = role

        Username = Username[:19]

        if Username == User_role.Admin.value:

            logging.info('.ثبت نام ادمین جدید\n')

            return Admin_application.Sign_up(role)







