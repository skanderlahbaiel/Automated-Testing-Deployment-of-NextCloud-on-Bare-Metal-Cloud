import time
from functional_testing.utils.user_management import perform_delete_user, check_user_absence, navigate_to_users_page
from functional_testing.config.configuration import OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, USERS_BUTTON_XPATH
from functional_testing.utils.authentication_management import orange_text

def delete_user(driver, username):
    """
    Deletes a specified user from the application and verifies their absence.

    This function navigates to the user management page, performs the deletion of a user based on the given username,
    and checks to ensure the user is no longer present in the application. It utilizes utility functions for navigation,
    user deletion, and verification of user absence. If the function encounters any exceptions during the process, it
    returns False, indicating the user was not successfully deleted.

    :param driver: An instance of Selenium WebDriver, used to automate browser interactions.
    :type driver: WebDriver
    :param username: The username of the user to be deleted. This is used to identify the specific user in the 
                     user management interface.
    :type username: str

    :return: Returns True if the user is successfully deleted and confirmed to be absent from the application.
             Returns False if the deletion process fails at any step or if the user is still present after the
             deletion attempt.
    :rtype: bool

    :raises Exception: Propagates any exceptions encountered during navigation, user deletion, or verification
                       of user absence. It logs the exception before re-raising, providing context for the error.

    .. note::
        - The function assumes that it's being called within the context of an authenticated session where
          the driver has access to the application's user management interface.
        - This function relies on external utility functions `navigate_to_users_page`, `perform_delete_user`,
          and `check_user_absence` for various steps of the process. Ensure these are correctly implemented
          and accessible in the project.

    **Example**::

        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> username = "testuser"
        >>> deletion_success = delete_user(driver, username)
        >>> print(deletion_success)
        True
    """

    try:
        ###! Add handling the situation where we are not in the user management page !###
        orange_text(f"Deleting user {username}...")
        navigate_to_users_page(driver, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, USERS_BUTTON_XPATH)
        perform_delete_user(driver, username)
        check_user_absence(driver, username)
        return True
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        return False