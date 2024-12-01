import logging
import os


def info_log(msg, user=os.getlogin()):
    logging.info(user + " - INFO - " + msg)


def warn_log(msg, user=os.getlogin()):
    logging.warning(user + " - WARNING - " + msg)


def debug_log(msg, user=os.getlogin()):
    logging.debug(user + " - DEBUG - " + msg)
