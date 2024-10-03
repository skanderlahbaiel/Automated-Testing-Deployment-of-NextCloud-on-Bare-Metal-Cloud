from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functional_testing.config.configuration import (
    LOGOUT_BUTTON_PATH,
    LOGIN_BUTTON_XPATH,
    OPEN_SETTINGS_MENU_XPATH,
    CLOSED_SETTINGS_MENU_XPATH,
    TARGET_URL
    )

from functional_testing.utils.authentication_management import(
    toggle_settings_menu, 
    green_text, 
    login_to_nextcloud,
    perform_logout,
    
)


from functional_testing.utils.file_management import (
    ensure_element_interactable,
    perform_file_upload,
    create_file
)

import random
import time
import secrets
import random
import string



#### User Creation ####


def generate_name():
    """Generate a random name-like string."""
    name_part = ''.join(secrets.choice(string.ascii_uppercase) + ''.join(secrets.choice(string.ascii_lowercase) for _ in range(random.randint(3, 5))))
    return 'test_' + name_part

def generate_email(username):
    """Generate an email address from a username."""
    domains = ["example.com", "test.org", "sample.net"]
    return f"{username}@{random.choice(domains)}"

def generate_password():
    """Generate a secure password."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(secrets.choice(characters) for _ in range(12))
    return password

def generate_user(group, quota, manager):
    """
    Generates a new user with specified credentials.

    Parameters:
        group (str): The group to which the user belongs.
        quota (str): The data quota assigned to the user.
        manager (str): The manager of the user.

    Returns:
        tuple: A tuple containing the generated user's username, display name, password, email, group, quota, and manager.
    """
    first_name = generate_name()
    last_name = generate_name()
    username = f"{first_name.lower()}{random.randint(10, 99)}"
    display_name = f"{first_name} {last_name}"
    password = generate_password()
    email = generate_email(username)

    return (username, display_name, password, email, group, quota, manager)

def click_users_button(driver, USERS_BUTTON_XPATH): 
    """
    Clicks on the "Users" button.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        USERS_BUTTON_XPATH (str): The XPath of the "Users" button.

    Returns:
        None
    """
    try:
        print("Clicking on users")
        users_button = driver.find_element(By.XPATH, USERS_BUTTON_XPATH)
        time.sleep(2)
        users_button.click()
        print("Users clicked")
        return  True
    except Exception as e:
        print(f"An error occurred while clicking on the users button: {e}")
        raise

def navigate_to_users_page(driver, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, USERS_BUTTON_XPATH):
    """
    Navigates to the users page.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        USERS_BUTTON_XPATH (str): The XPath of the "Users" button.

    Returns:
        None
    """
    try:
      print("Navigating to users page...")
      # Navigate to settings
      print("Navigating to settings")
      toggle_settings_menu(driver,OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, expected_state='open')
      # navigate to users button ( and ensure its clickable)
      print("Navigating to users")
      click_users_button(driver, USERS_BUTTON_XPATH)
      return  True
    except Exception as e:
        print(f"An error occurred while navigating to the users page: {e}")
        raise
             
def open_new_user_form(driver, NEW_USER_BUTTON):
    """
    Clicks on the "New user" button.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        NEW_USER_BUTTON (str): The ID of the "New user" button.

    Returns:
        None
    """
    try:
        new_user_button = driver.find_element(By.XPATH, NEW_USER_BUTTON)
        # click on new user button (ensure its interactable before)
        print("Clicking on new user button")
        time.sleep(2)
        new_user_button.click()
        return  True
    except Exception as e:
        print(f"An error occurred while clicking on the new user button: {e}")
        raise
    
def wait_then_click(driver, element):
    """
    Waits for the element to be clickable then clicks it.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The Selenium WebElement to click.

    Returns:
        None
    """
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
        element.click()
        return  True
    except Exception as e:
        print(f"An error occurred while waiting for the element to be clickable: {e}")
        raise
    
def wait_then_send_keys(driver, element, keys):
    """
    Waits for the element to be interactable then sends keys to it.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The Selenium WebElement to send keys to.
        keys (str): The keys to send to the element.

    Returns:
        None
    """
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
        element.send_keys(keys)
        return  True
    except Exception as e:
        print(f"An error occurred while waiting for the element to be clickable: {e}")
        raise

def fill_user_form(driver, username, display_name, password, email, group, quota, manager, NEW_USER_BUTTONS_XPATH):
    """
    Fills the user form with provided details in a NextCloud application.

    This function automates the process of filling out the user creation form in the NextCloud UI. 
    It inputs the provided user details into the form fields, selects the specified user group, and sets the user quota. 
    The function relies on a dictionary of XPaths to various form elements to interact with them.

    :param driver: The Selenium WebDriver instance used for browser automation.
    :type driver: WebDriver
    :param username: Username to be entered in the form.
    :type username: str
    :param display_name: Display name to be entered in the form.
    :type display_name: str
    :param password: Password to be entered in the form.
    :type password: str
    :param email: Email address to be entered in the form.
    :type email: str
    :param group: User group to be selected from a dropdown.
    :type group: str
    :param quota: User data quota to be entered in the form.
    :type quota: str
    :param manager: Manager's name to be entered in the form.
    :type manager: str
    :param NEW_USER_BUTTONS_XPATH: A dictionary mapping descriptive names to XPaths for interacting with the form.
    :type NEW_USER_BUTTONS_XPATH: dict

    :return: Indicates whether the user form was successfully filled.
    :rtype: bool

    :raises Exception: If an error occurs while filling the user form, providing the encountered error message.

    **Example**::

        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> username = "newuser"
        >>> display_name = "New User"
        >>> password = "securepassword"
        >>> email = "newuser@example.com"
        >>> group = "Users"
        >>> quota = "1GB"
        >>> manager = "admin"
        >>> NEW_USER_BUTTONS_XPATH = {
        ...     'NEW_USER_QUOTA_INPUT': 'xpath_here',
        ...     'NEW_USER_MANAGERS_INPUT': 'xpath_here',
        ...     # Add other necessary XPaths
        ... }
        >>> success = fill_user_form(driver, username, display_name, password, email, group, quota, manager, NEW_USER_BUTTONS_XPATH)
        >>> print(success)
        True
    """
    try:
        # Extract the XPaths from the **NEW_USER_BUTTONS_XPATH dictionary
        NEW_USER_QUOTA_INPUT = NEW_USER_BUTTONS_XPATH['NEW_USER_QUOTA_INPUT']
        NEW_USER_MANAGERS_INPUT = NEW_USER_BUTTONS_XPATH['NEW_USER_MANAGERS_INPUT']
        NEW_USER_MANAGERS_ADMIN = NEW_USER_BUTTONS_XPATH['NEW_USER_MANAGERS_ADMIN']
        NEW_USERNAME_INPUT = NEW_USER_BUTTONS_XPATH['NEW_USERNAME_INPUT']
        NEW_DISPLAY_NAME_INPUT = NEW_USER_BUTTONS_XPATH['NEW_DISPLAY_NAME_INPUT']
        NEW_USER_PASSWORD_INPUT = NEW_USER_BUTTONS_XPATH['NEW_USER_PASSWORD_INPUT']
        NEW_USER_EMAIL_INPUT = NEW_USER_BUTTONS_XPATH['NEW_USER_EMAIL_INPUT']
        NEW_USER_GROUP_DROPDOWN = NEW_USER_BUTTONS_XPATH['NEW_USER_GROUP_DROPDOWN']
        NEW_USER_ADMIN_GROUP = NEW_USER_BUTTONS_XPATH['NEW_USER_ADMIN_GROUP']
        NEW_USER_QUOTA_DROPDOWN = NEW_USER_BUTTONS_XPATH['NEW_USER_QUOTA_DROPDOWN']

        # Fill the form fields with the provided information
        print(f"Entering username: {username}")
        username_input = driver.find_element(By.XPATH, NEW_USERNAME_INPUT)
        wait_then_send_keys(driver, username_input, username)

        print(f"Entering display name: {display_name}")
        display_name_input = driver.find_element(By.XPATH, NEW_DISPLAY_NAME_INPUT)
        wait_then_send_keys(driver, display_name_input, display_name)

        print(f"Entering password: {password}")
        password_input = driver.find_element(By.XPATH, NEW_USER_PASSWORD_INPUT)
        wait_then_send_keys(driver, password_input, password)

        print(f"Entering email: {email}")
        email_input = driver.find_element(By.XPATH, NEW_USER_EMAIL_INPUT)
        wait_then_send_keys(driver, email_input, email)

        # Open the group dropdown
        print("Clicking on group dropdown")
        group_dropdown = driver.find_element(By.XPATH, NEW_USER_GROUP_DROPDOWN)
        wait_then_click(driver, group_dropdown)

        # Select the admin group
        admin_group = driver.find_element(By.XPATH, NEW_USER_ADMIN_GROUP)
        wait_then_click(driver, admin_group)
        print(f"Group selected: {group}")

        # Click on the username input to unfocus the group dropdown and allow the quota dropdown to be interactable
        username_input = driver.find_element(By.XPATH, NEW_USERNAME_INPUT)
        wait_then_click(driver, username_input)

        # Click on quota dropdown option
        print("Locating the quota dropdown element...")
        quota_dropdown = driver.find_element(By.XPATH, NEW_USER_QUOTA_DROPDOWN)
        print("Clicking on quota dropdown")
        wait_then_click(driver, quota_dropdown)

        quota_input = driver.find_element(By.XPATH, NEW_USER_QUOTA_INPUT)
        print(f"Quota entered: {quota}")
        wait_then_send_keys(driver, quota_input, quota)
        wait_then_send_keys(driver, quota_input, Keys.ENTER)

        # Click on managers input (ensure it's interactable before)
        managers_input = driver.find_element(By.XPATH, NEW_USER_MANAGERS_INPUT)
        print("Managers input found")
        print("Clicking on managers input")
        wait_then_send_keys(driver, managers_input, manager)

        # Click on the suggestion admin
        driver.find_element(By.XPATH, NEW_USER_MANAGERS_ADMIN).click()
        print(f"Managers input clicked {manager}")

        username_input = driver.find_element(By.XPATH, NEW_USERNAME_INPUT)
        wait_then_click(driver, username_input)

        return True

    except Exception as e:
        print(f"An error occurred while filling the user form: {e}")
        raise
       
def click_on_create_user(driver, NEW_USER_ADD_BUTTON):
    """
    Clicks on the "Create user" button.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        CREATE_USER_BUTTON_XPATH (str): The XPath of the "Create user" button.

    Returns:
        None
    """
    try:
      #submit_new_user (ensure its interactable before)
      print("Looking for add button")
      add_button = driver.find_element(By.XPATH, NEW_USER_ADD_BUTTON)
      print("Add button found")
      add_button.click()
      print("Add button clicked")
      time.sleep(1)
      return  True
    except Exception as e:
        print(f"An error occurred while clicking on the create user button: {e}")
        raise
       
def refresh_page(driver):
    """
    Refreshes the page.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.

    Returns:
        None
    """
    try:
        print("Refreshing the page...", flush=True)
        driver.refresh()
                # Wait for the page to finish loading
        WebDriverWait(driver, 15).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        return  True
    except Exception as e:
        print(f"An error occurred while refreshing the page: {e}")
        raise
       
def check_user_presence(driver, username):
    """
    Checks if the user is present in the user list.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        username (str): The username of the user to check for.

    Returns:
        bool: True if the user is present, False otherwise.
    """
    try:
        # Wait for the user to appear in the list
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@class='row' and @data-id='{username}']"))
            )
        green_text("Success, user creation succeeded")  
        
        return True
    except Exception as e:
        print(f"An error occurred while checking for the user presence: {e}")
        return False
    
def add_user_and_check_presence(driver, username, display_name, password, email, group, quota, manager, NEW_USER_BUTTONS_XPATH):
    """
    Adds a user to the application and verifies their presence in the user list.

    This function navigates the application's UI to add a new user with provided details.
    After adding, it attempts to locate the user in the application's user list to verify
    successful addition. If the user is found, the operation is considered successful.

    :param driver: WebDriver instance for interacting with the web application.
    :type driver: WebDriver
    :param username: The username of the new user.
    :type username: str
    :param display_name: The display name of the new user.
    :type display_name: str
    :param password: The password for the new user.
    :type password: str
    :param email: The email address of the new user.
    :type email: str
    :param group: The group to which the new user belongs.
    :type group: str
    :param quota: The quota assigned to the new user.
    :type quota: str
    :param manager: The manager of the new user.
    :type manager: str
    :param NEW_USER_BUTTONS_XPATH: A collection of keyword arguments mapping descriptive
        names to XPaths. These XPaths are used to interact with various UI elements
        necessary for user creation. Expected keys include:\n
        - OPEN_SETTINGS_MENU_XPATH: XPath to open the settings menu.\n
        - USERS_BUTTON_XPATH: XPath to access the users section.\n
        - NEW_USER_BUTTON: XPath to initiate new user creation.\n
        - NEW_USERNAME_INPUT: XPath for entering the user's username.\n
        - NEW_USER_ADD_BUTTON: XPath to finalize adding the new user.\n
    :type NEW_USER_BUTTONS_XPATH: dict

    :returns: True if the user is successfully added and found in the user list; returns False otherwise.
    :rtype: bool

    :raises Exception: Raises an exception if there's an issue during the user addition process
                       or while checking the user's presence.
    """
    try:
        # Navigate to users page
        navigate_to_users_page(driver, NEW_USER_BUTTONS_XPATH['OPEN_SETTINGS_MENU_XPATH'], NEW_USER_BUTTONS_XPATH['CLOSED_SETTINGS_MENU_XPATH'], NEW_USER_BUTTONS_XPATH['USERS_BUTTON_XPATH'])

        # Open new user form
        open_new_user_form(driver, NEW_USER_BUTTONS_XPATH['NEW_USER_BUTTON'])

        # Fill user form
        fill_user_form(driver, username, display_name, password, email, group, quota, manager, NEW_USER_BUTTONS_XPATH)

        # Click on create user button
        click_on_create_user(driver, NEW_USER_BUTTONS_XPATH['NEW_USER_ADD_BUTTON'])

        # Refresh the page
        refresh_page(driver)

        # Check if the user is present
        user_presence = check_user_presence(driver, username)
        assert user_presence, "The user was not found in the user list"

    except Exception as e:
        print(f"An error occurred while adding a user and checking for the user presence: {e}")
        raise
    
    
    
    
#### Delete User  ####

def check_presence_user_management_page(driver,OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, USERS_BUTTON_XPATH):
    """
    Checks if the user management page is open. Else, it opens the user management page."""
    try:
        if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-list-grid']"))):
            print("User management page found")
            return True
        else:
            print("User management page not found, navigating to users page...")
            navigate_to_users_page(driver, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, USERS_BUTTON_XPATH)
    except Exception as e:
        print(f"An error occurred while checking for the user management page: {e}")
        raise
    
def generate_user_xpath(username):
    """
    Generates the XPath for the user's main div based on the given username.

    Args:
        username (str): The username to generate the XPath for.

    Returns:
        str: The generated XPath.
    """
    return f"//div[@data-id='{username}']"

def generate_user_actions_button_xpath(username):
    """
    Generates the XPath for the user's actions button based on the given username.

    Args:
        username (str): The username to generate the XPath for.

    Returns:
        str: The generated XPath for the user's actions button.
    """
    return f"{generate_user_xpath(username)}//button[@aria-label='Toggle user actions menu']"

def generate_delete_user_button_xpath():
    """
    Generates the XPath for the user's "Delete user" button based on the given username.

    Args:
        username (str): The username to generate the XPath for.

    Returns:
        str: The generated XPath for the "Delete user" button.
    """
    return "//div[@class='popovermenu open']//button[@class='menuitem focusable']"

def generate_confirm_delete_user_button_xpath():
    """
    Generates the XPath for the confirmation button to delete a user. Assumes
    the confirmation button has a class that can be uniquely identified and does not depend on the username.

    Returns:
        str: The generated XPath for the confirmation button.
    """
    return "//button[@class='error primary']"

def perform_delete_user(driver, username):
    """
    Deletes a user from the user list.
    """
    try:
        # Click on the user's actions button
        print("\033[38;2;255;165;0mUser Deletion in progress...\033[0m")
        print("Generating the user's XPath")
        user_xpath = generate_user_xpath(username)
        print("Looking for the user element")
        user= driver.find_element(By.XPATH, user_xpath)
        print("Scrolling the user into view")
        ensure_element_interactable(driver, user)
        user_actions_button_xpath = generate_user_actions_button_xpath(username)
        print("User scrolled into view")
        print("Looking for the user's actions button")
        user_actions_button = driver.find_element(By.XPATH, user_actions_button_xpath)
        print("User's actions button found")
        user_actions_button.click()
        print("User's actions button clicked")
        time.sleep(5)

        # Click on the "Delete user" button
        print("generating delete user button")
        delete_user_button_xpath = generate_delete_user_button_xpath()
        print("Looking for the delete user button")
        delete_user_button = driver.find_element(By.XPATH, delete_user_button_xpath)
        print("Delete user button found")
        delete_user_button.click()
        print("Delete user button clicked")
        time.sleep(2)

        # Confirm the deletion
        confirm_delete_user_button_xpath = generate_confirm_delete_user_button_xpath()
        print("Looking for the confirm delete user button")
        confirm_delete_user_button = driver.find_element(By.XPATH, confirm_delete_user_button_xpath)
        print("Confirm delete user button found")
        confirm_delete_user_button.click()
        print("Confirm delete user button clicked")
        time.sleep(2)
        return  True
    except Exception as e:
        print(f"An error occurred while deleting the user: {e}")
        raise
    
def check_user_absence(driver, username):
 """
    Checks if the user is absent from the user list.

    Args:
        driver (WebDriver): The WebDriver instance used for interacting with the web page.
        username (str): The username of the user to check for absence.

    Returns:
        None

    Raises:
        AssertionError: If the user is not deleted or if any exception occurs during the process.
    """
 try:
        # We generate the XPath for the user's div instead of finding the element directly
        # because the element might not be present on the page, which would raise an exception.
        user_xpath = generate_user_xpath(username)
        
        # We refresh the page to ensure that we have the most up-to-date user list.
        # This is necessary because the user might have been deleted on the server side,
        # but the change might not be reflected on the client side yet.
        refresh_successful = refresh_page(driver)
        if not refresh_successful:
            print("Page refresh was not successful.")
            return
        # We wait for a specific element that indicates the page has fully loaded.
        # This is necessary because the user list might not be immediately available after the page refresh.
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "header"))
        )
        # We add a small delay to ensure that all elements have been rendered properly.
        # This is a workaround for potential timing issues between the browser and the WebDriver.
        time.sleep(1)
        # We check for the invisibility of the user's div instead of its absence
        # because the div might still be present in the DOM but hidden from the user.
        # This is a common practice in web development to hide elements instead of removing them.
        deletion = WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, user_xpath)))
        
        green_text("User deleted")
        # We use an assertion to ensure that the user was indeed deleted.
        # This makes the code fail fast, which is a good practice in testing.
        assert deletion, "The user was not deleted"
 except Exception as e:
        # We print the exception and re-raise it to ensure that it doesn't go unnoticed.
        # This is a good practice in exception handling to avoid silent failures.
        print(f"An error occurred while checking for the user absence: {e}")
        raise




   
def modify_quota(driver, username, quota, MODIFY_USER_BUTTON_XPATH, SAVE_MODIFICATION_BUTTON_XPATH):
    """
    Modify the quota for a user.

    :param driver: A webdriver object for interacting with the browser.
    :type driver: webdriver object
    :param username: The username of the user whose quota is to be modified.
    :type username: str
    :param quota: The new quota value.
    :type quota: str
    """
    
    def generate_modify_quota_input_xpath(username):
        """
        Generate the XPath for the quota input field of a user.

        :param username: The username of the user whose quota input field XPath is to be generated.
        :type username: str
        :return: The XPath for the quota input field of the user.
        :rtype: str
        """
        return f"//input[starts-with(@id, 'quota{username}')]"

    
    def scroll_horizontally(driver, xpath,timeout=20):
        """
        Scrolls the browser window horizontally to reveal an element.

        This function uses the WebDriver's built-in scrolling capabilities to scroll the browser window horizontally. It's useful when dealing with web pages that have elements outside the visible area or that are loaded dynamically..

        :param driver: A WebDriver instance representing the browser window.
        :type driver: selenium.webdriver.Remote
        :param element: The web element that the browser window should be scrolled to.
        :type element: selenium.webdriver.remote.webelement.WebElement
        """
        start_time = time.time()
        user_container = driver.find_element(By.XPATH, '//*[@id="app-content"]')
        while time.time() - start_time < timeout:
            try:
                if driver.find_element(By.XPATH, xpath):
                    return True
            except Exception:
                pass

            driver.execute_script("arguments[0].scrollLeft += 100", user_container)

        print(f"Timed out after {timeout} seconds while scrolling horizontally.")
        return False
    
    try:
        print("Looking for the modify user button")
        modify_user_button = driver.find_element(By.XPATH, MODIFY_USER_BUTTON_XPATH)
        print("Clicking on the modify user button")
        modify_user_button.click()
        print("generating user row xpath")
        print("Looking for the user row")
        print("Looking for the input field to modify the quota")
        quota_input_xpath = generate_modify_quota_input_xpath(username)        
        print(f"Quota input xpath: {quota_input_xpath}")
        #time.sleep(2000)
        ### Scroll horizontally to uncover the input field ###
        #scroll_horizontally(driver, quota_input_xpath, 20)
        quota_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, quota_input_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", quota_input)
        print("Clearing the quota input field")
        quota_input.clear()
        print("Entering the new quota value")
        quota_input.send_keys(quota)
        print("Submitting the new quota value")
        quota_input.send_keys(Keys.ENTER)
        #time.sleep(1000)
        save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, SAVE_MODIFICATION_BUTTON_XPATH)))
        print("Clicking on the save button")
        save_button.click()
        time.sleep(10)
        
        
    except Exception as e:
        print(f"An error occurred while modifying user quota: {e}")
        raise

def test_quota(driver, username, password):
    """test_quota _summary_

    _extended_summary_

    :param driver: _description_
    :type driver: _type_
    :param username: _description_
    :type username: _type_
    :param password: _description_
    :type password: _type_
    :param quota: _description_
    :type quota: _type_
    """
    try:
        print("Logging out...")
        perform_logout(driver, LOGOUT_BUTTON_PATH, LOGIN_BUTTON_XPATH, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH)
        print("Logging in as the user...")
        login_to_nextcloud(driver, TARGET_URL, username, password, LOGIN_BUTTON_XPATH)
        print("Uploading a file...")
        file_path, file_upload_id = create_file(1, directory="./created_files", base_name="test", extension=".txt")
        perform_file_upload(driver, file_path, file_upload_id)
        print("File uploaded successfully")
    except Exception as e:
        print(f"An error occurred while testing user quota: {e}")
        raise
    
    
     