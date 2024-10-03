from functional_testing.config.configuration import (
NEW_USER_BUTTONS_XPATH

)

from functional_testing.utils.user_management import (
add_user_and_check_presence
)
       
def add_user(driver, username, display_name, password, email, group, quota, manager):
    """
    Adds a new user to the application with specified attributes.

    This function utilizes the `add_user_and_check_presence` utility function from the
    `functional_testing.utils.user_management` module to create a new user in the application. It then verifies
    the presence of the newly added user to ensure successful creation. The process involves automating browser
    interactions using Selenium WebDriver to fill and submit the new user form with provided user details.

    :param driver: An instance of Selenium WebDriver, used for automating interactions with the web
                   application's interface.
    :type driver: WebDriver
    :param username: The username for the new user. Must be unique within the application.
    :type username: str
    :param display_name: The display name of the new user. This is the name that will be displayed within the
                         application's UI.
    :type display_name: str
    :param password: The password for the new user's account. Ensure compliance with application's password
                     policy.
    :type password: str
    :param email: The email address associated with the new user. Must be in a valid email format.
    :type email: str
    :param group: The group to which the new user will be assigned. Defaults to 'admin'.
                  Available groups may vary based on application configuration.
    :type group: str, optional
    :param quota: The storage quota assigned to the new user's account. Defaults to '1 GB'. The format
                  and available options may depend on application settings.
    :type quota: str, optional
    :param manager: The username of the user's manager. Defaults to 'admin'. This is relevant in
                    applications with hierarchical user management.
    :type manager: str, optional

    :returns: True if the new user is successfully added and their presence is verified within the application,
              False if the addition fails at any step or if the user cannot be verified post-creation.
    :rtype: bool

    :raises Exception: Propagates exceptions that may arise during the user creation or verification process, including
                       issues with browser automation or failures in interacting with the application's UI.

    Example::

        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> result = add_user(driver, "new_user", "New User", "securepassword", "new_user@example.com",
        ...                   "users", "2 GB", "senior_manager")
        >>> print(result)
        True

    Note:
        This function requires the `NEW_USER_BUTTONS_XPATH` dictionary from the
        `functional_testing.config.configuration` module, which contains XPaths for various UI elements involved in
        the user creation process.
    """
    try:
        add_user_and_check_presence(driver, username, display_name, password, email, group, quota, manager, NEW_USER_BUTTONS_XPATH)
        return True
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        return False
    
    
    