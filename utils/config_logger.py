# remote imports
import os
import logging
import time
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler
import functools
import uuid
import inspect

# local imports
from utils.info_system import get_user
from config.settings import LOG_PATH, LOG_DIR, LOCATE

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
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if record.exc_info:
            log_record['traceback'] = self.formatException(record.exc_info)

def setup_logger(name=__name__, locate_value=None):
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
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
        ' %(event_id)s' # execution unique ID 
        ' %(duration)s'  # execution duration
        ' %(source_file)s' # file/source that triggered the log
    )

    logHandler.setFormatter(formatter)

    end_user = get_user()
    context_filter = ContextFilter(user=end_user, locate=locate_value)
    logger.addFilter(context_filter)

    logger.addHandler(logHandler)

    return logger

def log_with_context(job=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            event_id = str(uuid.uuid4())
            source_file = inspect.getfile(func)

            logger = kwargs.get('logger')
            if logger is None:
                from utils.config_logger import setup_logger
                logger = setup_logger()

            try:
                result = func(*args, **kwargs)
                duration = round(time.time() - start_time, 2)

                logger.info(
                    f"{func.__name__} executed successfully",
                    extra={
                        'job': job or func.__name__,
                        'status': 'success',
                        'event_id': event_id,
                        'duration': duration,
                        'source_file': source_file
                    }
                )
                return result
            except Exception as e:
                duration = round(time.time() - start_time, 2)
                logger.exception(
                    f"error executing {func.__name__}: {e}",
                    extra={
                        'job': job or func.__name__,
                        'status': 'failure',
                        'event_id': event_id,
                        'duration': duration,
                        'source_file': source_file
                    }
                )
                raise

        return wrapper
    return decorator
