from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from functional_testing.utils.authentication_management import(
     orange_text,
     green_text,
     login_to_nextcloud,
     perform_logout,
     get_token_from_cookies,
     check_if_loggedIn,
     check_logout
)
from selenium.webdriver.common.keys import Keys
from functional_testing.config.configuration import LOGIN_BUTTON_XPATH, TARGET_URL

import hashlib
import time
import os
from datetime import datetime


def generate_file_share_button(driver, file_name):
    """
    Locates and returns the share button for a given file in a web page.

    Args:
        driver (WebDriver): The web driver instance controlling the browser.
        file_name (str): The name of the file for which to find the share button.

    Returns:
        WebElement: The share button element for the specified file.
        Returns None if the share button could not be found.
    """
    try:
        # Construct the XPath expression to locate the share button
        xpath = f"//tr[@data-file='{file_name}']//a[contains(@class, 'action-share')]"
        
        # Locate the share button using the constructed XPath
        share_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        
        return share_button
    except NoSuchElementException:
        # If no element is found, print a message and return None
        print(f"Share button not found for file '{file_name}'.")
        return None
    
    
### File Creation ### 
def create_testing_files(FILE_SIZE_MEDIUM, FILE_SIZE_LARGE, CREATED_FILES_PATH, TEST_FILE_BASE_MEDIUM, TEST_FILE_BASE_LARGE, EXTENSION):
    """
    Creates a medium size file and a large size file for testing purposes.

    Args:
        FILE_SIZE_MEDIUM (int): The size of the medium size file in bytes.
        FILE_SIZE_LARGE (int): The size of the large size file in bytes.
        CREATED_FILES_PATH (str): The path to the directory where the files will be created.
        base_name (str): The base name of the files.
        extension (str): The extension of the files.

    Returns:
        str: The path to the medium size file.
        str: The name of the medium size file.
        str: The path to the large size file.
        str: The name of the large size file.
    """
    medium_size_file_path, medium_size_file_name = create_file(FILE_SIZE_MEDIUM, directory=CREATED_FILES_PATH, base_name=TEST_FILE_BASE_MEDIUM, extension=EXTENSION)
    large_size_file_path, large_size_file_name = create_file(FILE_SIZE_LARGE, directory=CREATED_FILES_PATH, base_name=TEST_FILE_BASE_LARGE, extension=EXTENSION)
    return medium_size_file_path, medium_size_file_name, large_size_file_path, large_size_file_name

def extract_filename(file_path):
    """
    Extracts the filename from a given file path.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The filename extracted from the file path.
    """
    return file_path.split('/')[-1]

def extract_file_type(file_path):
    """
    Extracts the file type from the given file path.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The file type.

    Example:
        >>> extract_file_type('/path/to/file.txt')
        'txt'
    """
    return file_path.split('.')[-1]

def create_file(file_size_mb, directory="./created_files", base_name="test", extension=".txt"):
    """
    Creates a file of a specific size in megabytes in the specified directory with an automatically generated name.

    Args:
    file_size_mb (int): The size of the file in megabytes.
    directory (str): The directory where the file will be created.
    base_name (str): Base name for the file.
    extension (str): File extension.

    Returns:
    str: The path of the created file.
    str: The name of the created file.  
    """
    # Ensure the target directory exists
    os.makedirs(directory, exist_ok=True)

    # Convert size from MB to bytes
    file_size_bytes = file_size_mb * 1024 * 1024

    # Generate a unique file name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    file_name = f"{base_name}_{timestamp}{extension}"
    file_path = os.path.join(directory, file_name)

    # Create the file with the specified size
    with open(file_path, "wb") as file:
        file.write(b"\0" * file_size_bytes)

    # Return the path of the created file
    return file_path, file_name

### File Upload ###

def perform_file_upload(driver, file_path, file_upload_id):
    """
    Uploads a file and returns the XPath for checking its presence.

    Args:
        driver (WebDriver): The WebDriver instance.
        file_path (str): The path of the file to upload.
        file_upload_id (str): The ID of the file upload input element.

    Returns:
        str: The XPath for checking the presence of the uploaded file.
    """
    file_input = driver.find_element(By.ID, file_upload_id)
    orange_text(f"Uploading file to NexCloud from localhost. File path: {file_path}")
       
    file_input.send_keys(file_path)

    return f"//tr[@data-file='{extract_filename(file_path)}']"

def check_file_presence(driver, file_xpath, wait_time):
    """
    Checks if the uploaded file is present in NextCloud.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_xpath (str): The XPath expression to locate the file element.
        wait_time (int): The maximum time (in seconds) to wait for the file to be present.

    Returns:
        True if the file is present within the specified wait time, False otherwise.
    """
    try:
        # Wait for the file to apear in the list
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, file_xpath)))
        return True
    except TimeoutException:
        return False

def scroll_element_into_view(driver, element):
    """
    Scrolls the web page to bring the element into the viewport.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The Selenium WebElement to scroll into view.
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

def is_element_clickable(driver, element):
    """
    Checks if the web page element is clickable.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The Selenium WebElement to check for clickability.

    Returns:
        bool: True if the element is clickable, False otherwise.
    """
    try:
        # Adjust to wait for the specific element to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element.get_attribute('xpath'))))
        return True
    except (WebDriverException, TimeoutException):
        return False

def ensure_element_interactable(driver, element):
    """
    Ensures the element is in view and interactable by scrolling into view and checking clickability.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The Selenium WebElement to make interactable.
    """
    print("Scrolling the element into view", flush=True)
    scroll_element_into_view(driver, element)
    time.sleep(1)  # A brief pause to ensure the page has settled
    print("Checking if the element is clickable", flush=True)
    if is_element_clickable(driver, element):
        return True
    else:
        return False
            
### File Download ###    

def perform_download_file(driver, file_name, DOWNLOADS_PATH, max_wait_time=500, check_interval=5):
    """
    Downloads a file from NextCloud.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_name (str): The name of the file to download.
        DOWNLOADS_PATH (str): The path where the downloaded file will be saved.
        max_wait_time (int, optional): The maximum time (in seconds) to wait for the file to be downloaded. Defaults to 500.
        check_interval (int, optional): The interval (in seconds) between each check for the downloaded file. Defaults to 5.

    Raises:
        Exception: If the maximum wait time is exceeded while waiting for the file to download.

    Returns:
        None
    """
    
    #### Modify the function to locate the file element and not not the action menu button ####
    orange_text(f"Downloading {file_name} from NextCloud...")
    # Load the xPath of the file, waits for the actions button to be clickable, then clicks it to reveal the download button
    file_element_xpath = f"//tr[@data-file='{file_name}']"
    actions_menu_xpath = f"{file_element_xpath}//a[@data-action='menu']"
    file_element = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, file_element_xpath)))
    ensure_element_interactable(driver, file_element)
    file_element = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, actions_menu_xpath)))
    print(f"Element found ", flush=True)
    ensure_element_interactable(driver, driver.find_element(By.XPATH, actions_menu_xpath))
    time.sleep(2)
    actions_button = driver.find_element(By.XPATH, actions_menu_xpath)
    print("actions button found", flush=True)
    # Click to open the action menu
    time.sleep(2)
    print("Clicking the action menu", flush=True)
    time.sleep(2)
    actions_button.click()
    time.sleep(2)
    print("Action menu toggled, waiting for the download button to be clickable", flush=True)
    download_button_xpath = f"{file_element_xpath}//a[@data-action='Download']"
    ensure_element_interactable(driver, driver.find_element(By.XPATH, download_button_xpath))
    download_button = driver.find_element(By.XPATH, download_button_xpath)
    print("Download button found", flush=True)
    time.sleep(2)
    # Click the download button
    print("Clicking the download button", flush=True)
    download_button.click()
    print("Download button clicked, waiting for file to be downloaded", flush=True)
    # Dynamically wait for the file to be downloaded
    start_time = time.time()
    while True:
        # Check if the file exists
        downloaded_file_path = f"{DOWNLOADS_PATH}/{file_name}"
        if os.path.exists(downloaded_file_path):
            break

        # Check if the maximum wait time has been exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time > max_wait_time:
            raise Exception("Maximum wait time exceeded while waiting for file to download")

        # Wait for a short period before checking again
        print(f"Waiting for the file to download... Elapsed time: {elapsed_time:.2f} seconds", flush=True)
        time.sleep(check_interval)
        # Close the action menu    
    
        print(f"Checking if the file was downloaded to {downloaded_file_path}", flush=True)
        assert os.path.exists(downloaded_file_path), "The downloaded file was not found in the local directory"
       
def check_file_deletion(driver, file_element, wait_time):
    """
    Checks if the uploaded file is absent in NextCloud.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_element (WebElement): The WebElement instance of the file.
        wait_time (int): The maximum time (in seconds) to wait for the file to be absent.

    Returns:
        True if the file is absent within the specified wait time, False otherwise.
    """
    try:
        # Waits for the file to disappear from the list
        WebDriverWait(driver, wait_time).until(staleness_of(file_element))
        print("File deleted, no longer in Nexcloud UI", flush=True)
        return True
    except TimeoutException:
        return False
    
def calculate_sha256(file_path):
    """
    Calculate the SHA-256 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The SHA-256 hash of the file.
    """
    print((f"Calculating SHA-256 hash of file: {file_path}"), flush=True)
    # Initialize the hash object
    sha256_hash = hashlib.sha256()
    with open(file_path,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    # Return the hexadecimal digest        
    return sha256_hash.hexdigest()


def toggle_file_upload(driver, FILE_UPLOAD_START_ID):
    """
    Toggles the file upload window by revealing the file upload input element.

    Args:
        driver: The WebDriver instance used to interact with the browser.
        FILE_UPLOAD_START_ID: The ID of the file upload input element.

    Raises:
        AssertionError: If the upload field is not visible.

    Returns:
        None
    """
    try:
        # Reveal the file upload input element
        driver.execute_script(f'document.getElementById("{FILE_UPLOAD_START_ID}").classList.remove("hiddenuploadfield");')

        upload_field = driver.find_element(By.ID, FILE_UPLOAD_START_ID)
        # If the upload field is found, the navigation test passes. Else, it fails
        assert upload_field is not None, "The file upload window was not toggled."
        if upload_field is not None:
            print("File upload window toggled")
        else:
            print("Error, file upload window not toggled")
    except Exception as e:
        print(f"Error: {e}")

def click_new_fileOrFolder (driver,NEW_FILE_OR_FOLDER_MENU_XPATH ):
            new_button = driver.find_element(By.XPATH, NEW_FILE_OR_FOLDER_MENU_XPATH)
            new_button.click()

def check_files_container_presence(driver, timeout=10):
    """
    Checks if the specific element is present on the page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        timeout (int): Maximum time to wait for the element to be present.

    Returns:
        bool: True if the element is found within the timeout, False otherwise.
    """
    try:
        # Wait for the element to be present on the page.
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "app-content-files"))
        )
        print("Element found.")
        return True
    except:
        print("Element not found.")
        return False
    

            
def ensure_logged_in_and_goto_files(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH, FILES_TAB_XPATH):
    """
    This function checks if the the file container is present first, if it is then it passes to proceed to other tasks, else it logs in and navigates to the files page.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        TARGET_URL (str): The URL of the NextCloud instance.
        USERNAME (str): The username to use for logging in.
        PASSWORD (str): The password to use for logging in.
        LOGIN_BUTTON_XPATH (str): The XPath expression for the login button.
        FILES_TAB_XPATH (str): The XPath of the "Files" button.
        NEW_FILE_OR_FOLDER_MENU_XPATH (str): The XPath of the "New file/folder menu" button.

    Returns:
        None
    """

    try:
        # If not logged in, perform login
        if not check_if_loggedIn(driver, 5):
            print("User not logged in, logging in", flush=True)
            login_to_nextcloud(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH)
        else:
            # If logged in and file container present, pass
            if check_files_container_presence(driver, 5):
                print("User logged in and file container present, passing", flush=True)
                return

        # If not logged in or file container not present, navigate to the files page
        goto_files(driver, FILES_TAB_XPATH)

    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        raise


def goto_files(driver, FILES_TAB_XPATH):
    """
    Navigates to the files page and opens the file upload dialog.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        FILES_TAB_XPATH (str): The XPath of the "Files" button.
        NEW_FILE_OR_FOLDER_MENU_XPATH (str): The XPath of the "New file/folder menu" button.

    Raises:
        Exception: If an error occurs during navigation.

    Returns:
        None
    """
    try:
        print("Navigating to the files page", flush=True)
        files_button = driver.find_element(By.XPATH, FILES_TAB_XPATH)
        files_button.click()
        print("Files page button clicked", flush=True)


    except Exception as e:
        print(f"Navigation to files failed due to an error: {e}")
 
 
### Integrity Check ###        
        
def compare_hashes(file_name,DOWNLOAD_DIRECTORY,CREATED_FILES_PATH):
    """
    This function compares the SHA-256 hashes of the uploaded and downloaded files.

    It calculates the SHA-256 hash of both the uploaded and downloaded files and compares them. 
    If the hashes are not the same, it raises an AssertionError.

    Args:
        file_name (str): The name of the file.
        DOWNLOAD_DIRECTORY (str): The directory where the downloaded file is stored.
        CREATED_FILES_PATH (str): The directory where the uploaded file is stored.

    Returns:
        bool: True if the hashes are the same, False otherwise.

    Raises:
        Exception: If an error occurs while comparing the hashes.
    """
    try:
        dowloaded_file_path = f"{DOWNLOAD_DIRECTORY}/{file_name}"
        uploaded_file_path = f"{CREATED_FILES_PATH}/{file_name}"
        uploaded_file_hash = calculate_sha256(uploaded_file_path)
        downloaded_file_hash = calculate_sha256(dowloaded_file_path)
        assert uploaded_file_hash == downloaded_file_hash, "The uploaded and downloaded files have different hashes"
        return True
    except Exception as e:
        print(f"An error occured while comparing the hashes: {e}")
        raise
 
     
import time

### Deletion ###

def scroll_with_mouse_wheel(driver, element, deltaY=100):
    """
    Scroll within an element using the mouse wheel.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The element to scroll within.
        deltaY (int): The vertical scroll amount (positive scrolls down, negative scrolls up).
    """
    scroll_script = """
        var event = new WheelEvent('wheel', {
            'deltaY': arguments[1],
            'deltaMode': 0
        });
        arguments[0].dispatchEvent(event);
    """
    driver.execute_script(scroll_script, element, deltaY)


def scroll_to_bottom_dynamic(driver, timeout=60):
    try:
        scrollable_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]'))
        )
        driver.execute_script("arguments[0].focus();", scrollable_element)
        print(f"Element {scrollable_element} found and ready for scrolling.", flush=True)
        print("Files list element found and ready for scrolling.", flush=True)

        end_time = time.time() + timeout
        old_count = 0
        while time.time() < end_time: 
            print("Scrolling to the bottom of the page", flush=True)
            scroll_with_mouse_wheel(driver, scrollable_element, deltaY=800)
            print("Waiting for the files to load", flush=True)
            time.sleep(3) 
            new_count = len(driver.find_elements(By.CSS_SELECTOR, 'tbody.files-fileList > tr'))
            if new_count == old_count:
                # No new files loaded, assume end of list
                break
            else:
                old_count = new_count
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_element)
                time.sleep(1)  # Wait for files to load
    except Exception as e:
        print(f"An error occurred while scrolling: {e}", flush=True)

def find_delete_button(driver, file_name):
    """
    Finds the delete button of the file in NexcCloud UI.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_name (str): The name of the file to find.

    Returns:
        Web element: A tuple containing the WebElement instance of the delete button.
    """
    print("Waiting for the actions button to be clickable", flush=True)
    # Load the xPath of the file, waits for the actions button to be clickable, then clicks it to reveal the download button
    file_element_xpath = f"//tr[@data-file='{file_name}']"
    actions_menu_xpath = f"{file_element_xpath}//a[@data-action='menu']"
    ensure_element_interactable(driver, driver.find_element(By.XPATH, actions_menu_xpath))
    # Find the file_element
    file_element = driver.find_element(By.XPATH, file_element_xpath)
    WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, actions_menu_xpath)))
    actions_button = driver.find_element(By.XPATH, actions_menu_xpath)
    time.sleep(3)
    actions_button.click()
    print("Action menu clicked, waiting for the delete button to be clickable", flush=True)
    # Find the delete button for the file
    delete_button_xpath = "//div[contains(@class, 'fileActionsMenu')]//a[contains(@class, 'action-delete') and @data-action='Delete']"
    ensure_element_interactable(driver, driver.find_element(By.XPATH, delete_button_xpath))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
    delete_button = driver.find_element(By.XPATH, delete_button_xpath)
    time.sleep(3)
    
    return delete_button, file_element   
        
def perform_delete_file(driver, file_name):
    try:
        print("Scrolling to the bottom of the page to load the whole content ", flush=True)
        scroll_to_bottom_dynamic(driver)
        delete_button, file_element = find_delete_button(driver, file_name)
        delete_button.click()
        
        print("Delete button clicked", flush=True)
        # Wait for the file to disappear from the file list, if not, the test fails
        print("Checking if the file was deleted", flush=True)
        file_deleted = check_file_deletion(driver, file_element, 20)
        green_text("Success, file deleted")
        assert file_deleted, "large size file was not deleted"
        
        
    except Exception as e:
        print(f"An error occured while deleting the file: {e}")
        raise


### Locate file in the UI ###
def locate_file_in_nextcloud(driver, file_name):
    """
    Locates a file in NextCloud.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_name (str): The name of the file to locate.

    Returns:
        bool: True if the file is found, False otherwise.
    """
    try:
        # Wait for the file to appear in the list
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[@data-file='{file_name}']"))
        )
        file_element = driver.find_element(By.XPATH, f"//tr[@data-file='{file_name}']")
        scroll_element_into_view(driver, file_element)
        print("File found")
        return True
    except:
        print("File not found")
        return False

### File Sharing ### 





    
def share_file_with_recipient(driver, username, file_name, SHARE_WITH_ANOTHER_USER_INPUT_XPATH, SAVE_SHARING_BUTTON_XPATH):
    """
    Share a file with a recipient.

    Args:
        driver: The WebDriver instance.
        username: The username of the recipient.
        file_name: The name of the file to be shared.
        SHARE_WITH_ANOTHER_USER_INPUT_XPATH: The XPath of the input field for sharing with another user.
        SAVE_SHARING_BUTTON_XPATH: The XPath of the button to save the sharing.

    Raises:
        Exception: If an error occurs while locating and filling the search field.

    """
    try:
        # Wait for the search field to be interactable
        print("Waiting for the search field to be interactable")
        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, SHARE_WITH_ANOTHER_USER_INPUT_XPATH)))
        print("Search field is interactable")
        # Scroll the search field into view
        print("Scrolling the search field into view")
        ensure_element_interactable(driver, search_field)
        print(f"Filling the search field with the recipient's username: {username}")
        search_field.send_keys(username)
        time.sleep(2)
        search_field.send_keys(Keys.ENTER)
        print("Enter button clicked")
        time.sleep(1)
        print("Waiting for the save sharing button to be clickable")
        save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, SAVE_SHARING_BUTTON_XPATH)))
        print("Clicking the save sharing button")
        save_button.click()
        print("Save sharing button is clicked")
        print(f"File {file_name} shared with {username}")
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred while locating and filling the search field: {e}")
        raise
    

       

        



def ifLogin_delete_cookies(driver, TARGET_URL=TARGET_URL):
    """
    Checks whether the page contains the file name and the download button.

    Args:
        driver (WebDriver): The WebDriver instance used to interact with the browser.
        internal_share_link (str): The internal file sharing link to navigate to.

    Returns:
        bool: True if the page contains the file name and the download button, False otherwise.
    """
    try:
        print("Checking if logged in")
        check_login = get_token_from_cookies(driver)
        if check_login is not None:
            print("User is logged in, deleting cookies and refreshing the page")
            driver.delete_all_cookies()
            print("Cookies deleted")
            driver.get(TARGET_URL)
            print("Page refreshed")
            time.sleep(5)
            print("Checking if logged out")
            check_logout(driver, LOGIN_BUTTON_XPATH)
            return True
    except Exception as e:
        print(f"An error occurred while checking login status and deletin cookies: {e}")
        raise 
           


def check_url_login_page(driver):
    """
    Checks if the current URL is the login page.
    """
    try:
        url = driver.current_url
        print(f"Current URL: {url}")
        if "login" in url:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred while checking the URL: {e}")
        return False    
    
def get_internal_share_link(driver, INTERNAL_LINK_COPY_BUTTON_XPATH):
    """
    Gets the internal share link of a file.

    Args:
        driver: The WebDriver instance used to interact with the browser.
        INTERNAL_LINK_COPY_BUTTON_XPATH: The XPath of the internal link copy button.

    Returns:
        The internal share link of the file.

    Raises:
        Exception: If an error occurs while getting the internal share link.
    """
    try:
     
        print("Waiting for the internal share link button to be clickable")
        internal_share_link_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, INTERNAL_LINK_COPY_BUTTON_XPATH)))
        print("Internal share button is clickable")
        ensure_element_interactable(driver, internal_share_link_button)
        # Disable scrolling
        driver.execute_script("document.body.style.overflow = 'hidden';")
        driver.execute_script("document.documentElement.style.overflow = 'hidden';")
        print("Internal share link button is scrolled into view")
        internal_share_link_button.click()
        ### Get href from the button
        internal_share_link = internal_share_link_button.get_attribute("href")
        #internal_share_link = wait_for_clipboard_change(old_clipboard_content, timeout=10, check_interval=0.5)
        print("Internal share link button is clicked")  
        # Enable scrolling
        driver.execute_script("document.body.style.overflow = '';")
        driver.execute_script("document.documentElement.style.overflow = '';")
        return internal_share_link
    except Exception as e:
        print(f"An error occurred while getting the internal share link: {e}")
        raise
    
def get_external_share_link(driver, EXTERNAL_LINK_COPY_BUTTON_XPATH, EXTERNAL_LINK_COPY_BUTTON_XPATH_HREF):
    """
    Gets the external share link of a file.

    Args:
        driver: The WebDriver instance used to interact with the browser.
        EXTERNAL_LINK_COPY_BUTTON_XPATH: The XPath of the external link copy button.

    Returns:
        The external share link of the file.

    Raises:
        Exception: If an error occurs while getting the external share link.
    """
    try:
        print("Waiting for the external share link button to be clickable")
        external_share_link_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, EXTERNAL_LINK_COPY_BUTTON_XPATH)))
        ensure_element_interactable(driver, external_share_link_button)
        # Disable scrolling
        print("Disabling scrolling")
        driver.execute_script("document.body.style.overflow = 'hidden';")
        driver.execute_script("document.documentElement.style.overflow = 'hidden';")

        print("External share link button is clickable")
        external_share_link_button.click()
        ### Get href from the button
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, EXTERNAL_LINK_COPY_BUTTON_XPATH_HREF)))
        external_share_link = link.get_attribute("href")
        print("External share link button is clicked")
        # Enable scrolling
        print("Enabling scrolling")
        driver.execute_script("document.body.style.overflow = '';")
        driver.execute_script("document.documentElement.style.overflow = '';")       
        return external_share_link
    except Exception as e:
        print(f"An error occurred while getting the external share link: {e}")
        raise
    

def logout_and_goto_external_link(driver, LOGOUT_BUTTON_PATH,LOGIN_BUTTON_XPATH,OPEN_SETTINGS_MENU_XPATH,CLOSED_SETTINGS_MENU_XPATH, EXTERNAL_LINK):
    try:
        perform_logout(driver, LOGOUT_BUTTON_PATH, LOGIN_BUTTON_XPATH, OPEN_SETTINGS_MENU_XPATH, CLOSED_SETTINGS_MENU_XPATH)
        driver.get(EXTERNAL_LINK)
    except Exception as e:
        print(f"An error occurred while logging out: {e}")
        raise
    
def check_external_file_sharing(driver, file_name):
    """
    Checks whether the page contains the file name and the download button.
    """
    try:
        print("Checking for the external file sharing")
        check_element_x_path = generate_external_share_verification_element(driver, file_name)
        print(f"Checking for the external file sharing: {check_element_x_path}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, check_element_x_path)))
        green_text("File found, external file sharing succeeded")
        return True
    except Exception as e:
        print(f"An error occurred while checking for the external file sharing: {e}")
        raise

def generate_external_share_verification_element(driver, file_name):
    """
    Generates the XPath for the verification element for external file sharing.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_name (str): The name of the file to generate the XPath for.

    Returns:
        str: The generated XPath for the verification element.
    """
    return f"//span[contains(text(), '{file_name}')]"

def check_internal_file_share(driver, file_name, internal_share_link, username, password, LOGIN_BUTTON_XPATH):
    """
    """
    try:
      print('Checking for the internal file sharing...')
      # Ensure that the user is logged out when accessing the internal share link
      ifLogin_delete_cookies(driver)
      # Navigate to the internal share link
      driver.get(internal_share_link)  
      # Check that the file is not accessible to the public
      if check_url_login_page(driver):
          green_text("Success, internal share link not accessible to the public")
          
      else:
          raise Exception("Internal share link accessible to the public")
      # Login to nextcloud using the internal share link and check if the file is accessible
      login_to_nextcloud(driver, internal_share_link, username, password, LOGIN_BUTTON_XPATH)
      check_internal_sharing(driver, file_name)
      # Login as another user and check if the file is accessible
      
      
        
    except Exception as e:
        print(f"An error occurred while checking for the internal file sharing: {e}")
        return False
       
def generate_internal_sharing_verification_element_exists(file_name):
    """
    Generates the XPath for the verification element for internal file sharing.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        file_name (str): The name of the file to generate the XPath for.

    Returns:
        str: The generated XPath for the verification element.
    """
    xpath = f"//div[contains(@class, 'modal-header')]//h2[contains(text(), '{file_name}')]"
    return xpath
    
def check_internal_sharing(driver, file_name):
    """
    """
    try:
        print("Checking for the internal file sharing...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, generate_internal_sharing_verification_element_exists(file_name))))
        green_text("File found, internal file sharing succeeded")
        return True
    except Exception as e:
        print(f"An error occurred while checking for the internal file sharing: {e}")
        raise