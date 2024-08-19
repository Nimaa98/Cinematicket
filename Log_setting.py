
import logging


def Log_config()->None:

    logging.basicConfig(
        filename= 'CinemaTicket.log',
        level = logging.INFO,
        format = '%(asctime)s - %(levelname)s - %(message)s'
    )