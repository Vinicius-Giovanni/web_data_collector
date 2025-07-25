import os
import logging
import time
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

from utils.info_system import get_user
from config.settings import LOG_PATH, LOG_FILE, LOCATE

class ContextFilter(logging.Filter):
    """
    filter that injecs the username into the log record 
    """
    def __init__(self, user=None, locate=None):
        super().__init__()
        self.user = user or get_user()
        self.locate = locate or LOCATE

    def filter(self, record):
        record.user = self.user
        record.locate = self.locate
        return True

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    asctime formatting
    """
    def formatTime(self, record, datefmt=None):
        return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(record.created))

def setup_logger(locate_value=None):
    os.makedirs(LOG_FILE, exist_ok=True)

    logger = logging.getLogger("web_data_collector")
    logger.setLevel(logging.INFO)

    logHandler = RotatingFileHandler(LOG_PATH, maxBytes=10 * 1024 * 1024, backupCount=5)

    formatter = CustomJsonFormatter(
        fmt='%(asctime)s' # exact date/time of the event
        ' %(levelname)s' # log level (INFO, WARNING, ERROR, etc.)
        ' %(name)s' # name of the logger
        ' %(message)s' # the actual log message
        ' %(job)s' # name of the job
        ' %(status)s' # status of the job (success, failure, etc.)
        ' %(user)s' # user or system resposible for execution
        ' %(locate)s' # operating system
    )

    logHandler.setFormatter(formatter)

    end_user = get_user()
    context_filter = ContextFilter(user=end_user, locate=locate_value)
    logger.addFilter(context_filter)

    logger.addHandler(logHandler)

    return logger