"""
Login Module

This module is responsible for the automated extraction of authentication data from the CSI system using Selenium with the chrome browser.
Its primary objective is o perform login securely and reliably, capturing session cookies that will be used by subsequent functions
to manage and controll multiple browser instances during data extractionand processing workflows.

Main functionalities:
- Initialization of the Chrome driver with configurations suitable for automated execution.
- Execution of the login process in CSI, including handling of username, password, and potential additional authentication challenges.
- Capture and storage of valid session cookies.
- Provision of cookies to other functions or classes, allowing session reuse without the need for a new login.
- Integration with instance-controlling functions, facilitating the management of multiple simultaneous downloads or distributed scraping processes.

Architectural benefits:
- Centralization of authentication logic, avoiding duplication in other modules.
- Efficiency in executing pipelines that rely on authenticated sessions.
- Greater robustness and simplified maintenance, as changes to the login process are handled in a single point.

"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
import locale

from utils.config_logger import setup_logger, log_with_context
from config.settings import LINKS, ELEMENTS, PASSWORD, EMAIL, FEATURE_WEB_DATA_COLLECTOR
from utils.reader import clear_dirs# falta
from utils.browser_setup import init_browser# falta
from utils.get_info import get_business_yesterday, get_yesterday_date# falta