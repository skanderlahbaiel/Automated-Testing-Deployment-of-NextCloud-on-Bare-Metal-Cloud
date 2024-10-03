from functional_testing.config.configuration import OPEN_SETTINGS_MENU_XPATH, LOGOUT_BUTTON_PATH, CLOSED_SETTINGS_MENU_XPATH, LOGIN_BUTTON_XPATH
from functional_testing.utils.authentication_management import toggle_settings_menu, click_on_logout, check_logout, orange_text
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

def logout(driver):
    """
    Performs logout from the application using the provided WebDriver instance.

    This function navigates the application's UI to log out the currently authenticated user. It specifically
    handles the UI interactions required to open the settings menu, click the logout button, and verify the logout
    process by checking for the presence of the login button. It uses a series of utility functions tailored to
    interact with specific UI elements defined in the configuration module.

    :param driver: An instance of Selenium WebDriver. This is used to automate the interaction with
                    the web browser, enabling the function to perform actions like clicking and checking
                    the presence of UI elements.
    :type driver: WebDriver

    :return: Indicates the outcome of the logout attempt. Returns True if the logout process is completed
              successfully, evidenced by the appearance of the login button. Returns False if the logout
              process fails at any step, either due to UI elements not being found or other exceptions.
    :rtype: bool

    :raises NoSuchElementException: Raised if any expected UI element involved in the logout process is not found
                                    within the current page. This exception points to possible changes in the UI or
                                    an incorrect navigation state.
    :raises Exception: A generic exception is raised for any other errors encountered during the logout process.
                       The function catches and logs these exceptions, providing a message detailing the encountered
                       issue.

    .. code-block:: python

        Example:
            driver = webdriver.Chrome()
            logout_success = logout(driver)
            if logout_success:
                print("Successfully logged out.")
            else:
                print("Logout failed.")

    .. note::
        The function assumes that the user is already logged in and that the WebDriver instance (`driver`) is in a
        state that allows direct interaction with the application's logout functionality. It relies on accurate
        XPath locators for the settings menu and logout button, specified in `OPEN_SETTINGS_MENU_XPATH`, 
        `CLOSED_SETTINGS_MENU_XPATH`, and `LOGOUT_BUTTON_PATH`, which should be configured in the
        `functional_testing.config.configuration` module before invoking this function.
    """
    def logout(driver):
        try:
            orange_text("Logging out...")
            
            # Toggle settings menu
            toggle_settings_menu(driver, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, expected_state='open')
                
            # Click the logout button
            click_on_logout(driver, LOGOUT_BUTTON_PATH)

            # Wait for the login button to appear
            if check_logout(driver, LOGIN_BUTTON_XPATH):
                return True
        except NoSuchElementException:
            print("Element not found")
            return False
        except Exception as e:
            print(f"An error occurred: {e}", flush=True)
            return False
    try:
        orange_text("Logging out...")
        
        # Toggle settings menu
        toggle_settings_menu(driver, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, expected_state='open')
            
        # Click the logout button
        click_on_logout(driver, LOGOUT_BUTTON_PATH)

        # Wait for the login button to appear
        if check_logout(driver, LOGIN_BUTTON_XPATH):
            return True
    except NoSuchElementException:
        print("Element not found")
        return False
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        return False