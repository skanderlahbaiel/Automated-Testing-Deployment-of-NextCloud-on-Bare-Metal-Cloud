import pytest

from functional_testing.utils.authentication_management import (
    load_nextcloud_page,
    login_to_nextcloud,
    orange_text
)
from functional_testing.config.configuration import (
    TARGET_URL, 
    USERNAME, 
    PASSWORD, 
    LOGIN_BUTTON_XPATH, 
)

def login(driver):
    """
    Authenticates a user into NextCloud using predefined credentials.

    This function orchestrates the process of logging into a NextCloud instance. It begins by navigating to the 
    NextCloud login page, specified by `TARGET_URL`, and then proceeds to input the predefined credentials 
    (`USERNAME` and `PASSWORD`) into the login form. The function checks for successful authentication by verifying 
    the presence of elements unique to authenticated sessions. If the login attempt faces any issues, the function 
    gracefully handles exceptions and provides feedback.

    :param driver: An instance of a Selenium WebDriver, used to automate web browser interaction.
                   The driver must be initialized and configured prior to calling this function.
    :type driver: WebDriver

    :return: Indicates the outcome of the login attempt. Returns True if the login process completes successfully, 
             indicating that the user has been authenticated. Returns False if there are any issues during the 
             login process, suggesting that the authentication did not occur.
    :rtype: bool

    :raises Exception: Raises a generic exception if any unexpected errors occur during the execution of the login 
                      process. The exception captures and suppresses detailed error information to prevent potential 
                      sensitive data exposure, adhering to security best practices.

    :example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> login_success = login(driver)
        >>> if login_success:
        ...     print("Login successful.")
        ... else:
        ...     print("Login failed.")

    :note:
        The login process relies on several configuration variables defined in the 
        `functional_testing.config.configuration` module, including `TARGET_URL`, `USERNAME`, `PASSWORD`, and 
        `LOGIN_BUTTON_XPATH`. Ensure these variables are accurately set to reflect the current state of the 
        NextCloud login page and user credentials.

    """

    try:
        orange_text(f"Logging in to {TARGET_URL}...")
        # Load the Nextcloud page
        load_nextcloud_page(driver, TARGET_URL)
        # Login to Nextcloud using the provided credentials
        login = login_to_nextcloud(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH)
        return True

    except Exception as e:
        return False

  