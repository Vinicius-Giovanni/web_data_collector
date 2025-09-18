"""
config_logger Module

This module provides a robust framework for configuring, formatting, and utilizing logs within the project,
adhering to corporate best practices for traceability and auditing. It centralizes logger creation, defines 
custom JSON formaing, and allows injection of corporate context (such as user, execution location, job, and exection details)
into each log entry.

Architectural benefits:
- Centralization of logging configuration, ensuring consistency and standardization.
- Facilitates monitoring, auditing, and debugging with full process context.
- Supports scalability and integration wih complex pipelines without altering individual functions.
- Reduces the risk of log inconsistency and duplicate configuration across multiple modules.

"""

import os
import logging
import time
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler
import functools
import uuid
import inspect
from utils.info_system import get_user
from config.settings import LOG_PATH, LOG_DIR

class ContextFilter(logging.Filter):
    """
    - A class extending logging.Filter to inject context information (user and location) into each log entry.
    - Ensures all logs containt consistent metadata for auditing and monitoring.
    """

    def __init__(self, user=None, locate=None):
        super().__init()
        self.user = user or get_user()

    def filter(self, record):
        record.user = self.user
        return True

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    - A subclass of jsonlogger.JsonFormatter that formats timestamps and adds additional fields.
    - Includes exception traceability via traceback whe applicable.
    - Maintains a consistent JSON log standard, faciliating ingestion into monitoring pipelines and dashboards.
    """

    def formatTime(self, record, datefml=None):
        return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(record.created))
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if record.exc_info:
            log_record['traceback'] = self.formatException(record.exc_info)

def setup_logger(name=__name__, locate_value=None):
    """
    - Function responsible for creating and configuring a logger wih a rotating handler.
    - Defines log level, storage path, formatting, and context filters.
    - Ensures log directories exist and prevents duplicate handlers.
    - Includes consistency verification of the created logger.
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        logHandler = RotatingFileHandler(LOG_PATH, maxBytes=10 * 1024 *1024, backupCount=5)

        formatter = CustomJsonFormatter(
            fmt=' '.join([
            '%(asctime)s', # exact date/time of the event
            '%(levelname)s', # log level (INFO, WARNING, ERROR, etc.)
            '%(name)s', # name of the logger
            '%(message)s', # the actual log message
            '%(job)s', # name of the job
            '%(status)s', # status of the job (success, failure, etc.)
            '%(user)s', # user or system resposible for execution
            '%(locate)s', # operating system
            '%(event_id)s', # execution unique ID 
            '%(duration)s',  # execution duration
            '%(source_file)s' # file/source that triggered the log
        ]))
        logHandler.setFormatter(formatter)

        context_filter = ContextFilter(user=get_user(), locate=locate_value)
        logger.addFilter(context_filter)
        logger.addHandler(logHandler)

    if not logger or not isinstance(logger, logging.Logger):
        raise RuntimeError(f'logger inválido criado para {name}')
    
    return logger

def log_with_context(job=None, logger=None):
    """
    - Decorator for functions that require structured logging with corporate context.
    - Capturess metrics such as execution time, unique event ID, execution status, and source file.
    - Allows fallback to a default logger if none is explicitly provided.
    - Facilitates detailed, standardized traceability across the application.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            event_id = str(uuid.uuid4())
            source_file = inspect.getfile(func)

            _logger = logger or kwargs.get('logger')
            if _logger is None:
                _logger = setup_logger(name='default_logger') # fallback

            try:
                result = func(*args, **kwargs)
                duration = round(time.time() - start_time, 2)

                _logger.info(
                    f"{func.__name__} executado com sucesso",
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
                _logger.exception(
                    f"erro de execução em {func.__name__}",
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