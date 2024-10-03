
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException 
import time
from functional_testing.config.configuration import LOGIN_BUTTON_XPATH 



### Green and Orange Logs ###

def orange_text(text):
     print(f"\033[38;2;255;165;0m{text}\033[0m", flush=True)

def green_text(text):
    print(f"\033[92m{text}\033[0m", flush=True)     

### Login ###

def check_if_loggedIn(driver, wait_time):
    """
    Checks if the user is logged in by verifying the presence of a token in the cookies.

    Args:
        driver: The Selenium WebDriver instance.
        wait_time: The maximum time to wait for the user to be logged in, in seconds.

    Returns:
        True if the user is logged in, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < wait_time:
        try:
            print("Checking if the user is logged in", flush=True)
            if get_token_from_cookies(driver):
                print("User is logged in", flush=True)
                return True
            else:
                pass
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e 
    print("User is not logged in", flush=True)
    return False

def get_token_from_cookies(driver):
    """
    Retrieves the 'nc_token' from the browser cookies.

    Args:
        driver (WebDriver): The web driver instance controlling the browser.

    Returns:
        str: The value of 'nc_token' if found, None otherwise.
    """
    try:
        # Retrieve all cookies
        cookies = driver.get_cookies()
        # Look for sesion cookie
        for cookie in cookies:
            if cookie['name'] == 'oc_sessionPassphrase':
                print(f"Session token found: {cookie['value']}")
                return cookie['value']
        
        
        print("User logged out or not logged in")
        return None
    except Exception as e:
        print(f"An error occurred while retrieving session token: {e}")
        return None


def check_successful_page_load(driver, wait_time):
    """
    Checks if the page load is successful by verifying the presence of specific elements on the page.

    Args:
        driver (WebDriver): The WebDriver instance used for interacting with the browser.
        wait_time (int): The maximum time to wait for the elements to load, in seconds.

    Returns:
        str: The ID of the first element that successfully loads within the specified wait time.
             If none of the elements load within the wait time, returns None.
    """

    elements_ids = ["body-login", "app-dashboard"]
    element_loaded = None
    start_time = time.time()
    while element_loaded is None and time.time() - start_time < wait_time:
        for element_id in elements_ids:
            try:
                element_loaded = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.ID, element_id))
                )
                break
            except TimeoutException:
                print(f"Element {element_id} not found")
                
            
    if element_loaded:
        return True
    else: raise TimeoutException("The page load was not successful")
            
       
    
def load_nextcloud_page(driver, TARGET_URL):
    """
    Loads the NextCloud page.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        TARGET_URL (str): The URL of the NextCloud instance.

    Returns:
        None
    """
    print(f"Loading NextCloud page: {TARGET_URL}", flush=True)
    driver.get(TARGET_URL)
    element = check_successful_page_load(driver, 10)
    # If the element is found, the login test passes. Else, it fails
    assert element is not None, "The app-dashboard element was not found."
    if element is not None:
        print("\nNextCloud page loaded successfully", flush=True)
    else:
        print("\nLoading Nexcloud web page failed page failed", flush=True)
    
def login_to_nextcloud(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH):
    """
    Fills the login form, submits and checks for successful login.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        TARGET_URL (str): The URL of the NextCloud instance.
        USERNAME (str): The username to use for logging in.
        PASSWORD (str): The password to use for logging in.
        LOGIN_BUTTON_XPATH (str): The XPath expression for the login button.

    Returns:
        bool: True if the login is successful, False otherwise.
    """
    
    print(f"Logging into NextCloud. URL: {TARGET_URL}, Username: {USERNAME}, Password: {PASSWORD}", flush=True)
    # Wait up to 10 seconds for the username input field to appear
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user")))
    # Wait up to 10 seconds for the password input field to appear
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))

    # Enter the username and password
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    
    # Wait for the login button to be clickable
    login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
    WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH)))
    login_button.click()
    time.sleep(5)
    # Check successful login
    element = check_if_loggedIn(driver, 30) ### bug with login when passing from share to delete
    # If the element is found, the login test passes. Else, it fails
    assert element is not None, "Login failed"
    if element is not None:
        try:
            print("Checking the welcome modal", flush=True) 
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'modal-description-lyiks')))
            close_button = driver.find_element(By.CSS_SELECTOR, '#modal-description-lyiks .modal-container__close')
            close_button.click()
            print("Close button clicked", flush=True)
            green_text("Login succeeded") 
            return True
        except TimeoutException:
            print("Modal did not appear", flush=True)
            green_text("Login succeeded")
            return True
    else:
        print("Login failed", flush=True)
        return False

    # This test navigates to the files page and opens the file upload dialog, its purpose is to verify that uploading button is visible

### Logout ###

def toggle_settings_menu(driver,OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, expected_state='open'):
    """
    Toggles the settings menu to the expected state ('open' or 'closed').

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        expected_state (str): The expected state of the settings menu. Defaults to 'open'.
    """
    settings_menu_open = bool(driver.find_elements(By.XPATH, OPEN_SETTINGS_MENU_XPATH))
    settings_menu_closed = bool(driver.find_elements(By.XPATH, CLOSED_SETTINGS_MENU_XPATH))
    
    if expected_state == 'open' and settings_menu_closed:
        driver.find_element(By.XPATH, CLOSED_SETTINGS_MENU_XPATH).click()
    elif expected_state == 'closed' and settings_menu_open:
        driver.find_element(By.XPATH, OPEN_SETTINGS_MENU_XPATH).click()
        
        
def click_on_logout(driver, LOGOUT_BUTTON_PATH):
    """
    Clicks on the logout button.

    Args:
        driver (WebDriver): The WebDriver instance used to interact with the browser.
        LOGOUT_BUTTON_PATH (str): The XPath of the logout button element.

    Returns:
        None
    """
    try:
        print("looking for the logout button")
        logout_button = driver.find_element(By.XPATH, LOGOUT_BUTTON_PATH)
        print("Scrolling to the logout button")
        time.sleep(1)
        
        print("Clicking the logout button")
        logout_button.click()
        print("Logout button clicked")
        return True
    except Exception as e:
        print(f"An error occurred while clicking the logout button: {e}")
        raise

def check_logout(driver, LOGIN_BUTTON_XPATH=LOGIN_BUTTON_XPATH):
    """
    Checks if the user has successfully logged out by waiting for the login button to appear.

    Args:
        driver: The WebDriver instance used for interacting with the browser.
        LOGIN_BUTTON_XPATH: The XPath of the login button element.

    Returns:
        True if the logout was successful, False otherwise.
    """
    try:
        print("Waiting for the login button to appear")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH)))
        green_text("Logout successful")
        return True
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        return False
    
def perform_logout(driver, LOGOUT_BUTTON_PATH, LOGIN_BUTTON_XPATH, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH):
    """
    Logs out of NextCloud.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        LOGOUT_BUTTON_PATH (str): The XPath of the logout button element.
        LOGIN_BUTTON_XPATH (str): The XPath of the login button element.

    Returns:
        bool: True if the logout is successful, False otherwise.
    """
    try:
        ### Add a check (check token existence) to see if the user is logged in or not ###
        toggle_settings_menu(driver,OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH, expected_state='open')        
        click_on_logout(driver, LOGOUT_BUTTON_PATH)
        return check_logout(driver, LOGIN_BUTTON_XPATH)
    except Exception as e:
        print(f"An error occurred while logging out: {e}")
        return False
    raise
