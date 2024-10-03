import time
from functional_testing.utils.file_management import(
    ensure_logged_in_and_goto_files, 
    locate_file_in_nextcloud,
    get_internal_share_link,
    get_external_share_link,
    logout_and_goto_external_link,
    check_external_file_sharing,
    check_internal_file_share,
    share_file_with_recipient,
    login_to_nextcloud,
    ifLogin_delete_cookies,
    orange_text,
    generate_file_share_button,
    scroll_element_into_view,
    ensure_element_interactable,
    
    )


from functional_testing.config.configuration import (
TARGET_URL, 
USERNAME,
PASSWORD,
FILES_TAB_XPATH,
SHARE_BUTTON_XPATH,
INTERNAL_LINK_COPY_BUTTON_XPATH, 
EXTERNAL_LINK_COPY_BUTTON_XPATH,
LOGOUT_BUTTON_PATH,
LOGIN_BUTTON_XPATH,
OPEN_SETTINGS_MENU_XPATH,
CLOSED_SETTINGS_MENU_XPATH,
SHARE_WITH_ANOTHER_USER_INPUT_XPATH,
SAVE_SHARING_BUTTON_XPATH,
EXTERNAL_LINK_COPY_BUTTON_XPATH_HREF
)


def locate_and_click_share_button(driver, file_name):
    """
    Shares a specified file internally and externally within NextCloud.

    This function handles multiple steps to share a file stored in NextCloud. Initially, it navigates
    to the files management page, locates the desired file, and then initiates the sharing process. It performs both
    internal sharing with a specified recipient and generates external sharing links. The function also validates 
    the accessibility of these shared links by simulating external access to ensure that the sharing functionality 
    works as expected.

    Args:
        driver (WebDriver): An instance of Selenium WebDriver used for automating browser interactions. It must be
                            initialized and configured before being passed to this function.
        username (str): The username of the recipient with whom the file will be shared internally. This user must
                        exist within the NextCloud system.
        password (str): The password for the above username, used to validate internal sharing functionality by
                        attempting to access the shared file.
        file_name (str): The name of the file to be shared. The file should already exist in the NextCloud directory
                         that the initiating user has access to.

    Returns:
        bool: True if both internal and external sharing links are generated and validated successfully, indicating
              that the file has been shared properly. Returns False if any step in the sharing or validation process
              fails.

    Raises:
        Exception: If an error occurs at any point during the file sharing process, including issues with locating
                   the file, sharing operations, link generation, or access validations. The specific error message
                   is printed to the console.

    Example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> username = "example_user"
        >>> password = "password123"
        >>> file_name = "document.pdf"
        >>> share_success = share_file(driver, username, password, file_name)
        >>> if share_success:
        ...     print("File shared successfully.")
        ... else:
        ...     print("File sharing failed.")

    Note:
        - This function assumes that the user initiating the share (typically an admin or the file owner) is
          logged into NextCloud at the start of the function.
        - The function performs a logout operation as part of its external link validation step, and then logs
          back in as the admin user. Ensure that any necessary session data is saved or that subsequent operations
          account for this logout/login cycle.
    """
    try:
        # Wait for the share button to be clickable
        print("Waiting for the share button to be clickable")
        share_button = generate_file_share_button(driver, file_name)
        print("Share button is clickable")
        # Scroll the share button into view
        print("Scrolling the share button into view")
        scroll_element_into_view(driver, share_button)
        ensure_element_interactable(driver, share_button)
        # Click the share button
        print("Clicking the share button")
        share_button.click()
        print("Share button is clicked")

    except Exception as e:
        print(f"An error occurred while locating and clicking the share button: {e}")
        raise
    
def share_file(driver, username, password, file_name, LOGIN_BUTTON_XPATH=LOGIN_BUTTON_XPATH):
    """
    Shares a specified file internally and externally within NextCloud.

    This comprehensive function handles multiple steps to share a file stored in NextCloud. Initially, it navigates
    to the files management page, locates the desired file, and then initiates the sharing process. It performs both
    internal sharing with a specified recipient and generates external sharing links. The function also validates 
    the accessibility of these shared links by simulating external access to ensure that the sharing functionality 
    works as expected.

    :param driver: An instance of Selenium WebDriver used for automating browser interactions. It must be
                   initialized and configured before being passed to this function.
    :type driver: WebDriver
    :param username: The username of the recipient with whom the file will be shared internally. This user must
                     exist within the NextCloud system.
    :type username: str
    :param password: The password for the above username, used to validate internal sharing functionality by
                     attempting to access the shared file.
    :type password: str
    :param file_name: The name of the file to be shared. The file should already exist in the NextCloud directory
                      that the initiating user has access to.
    :type file_name: str

    :return: True if both internal and external sharing links are generated and validated successfully, indicating
             that the file has been shared properly. Returns False if any step in the sharing or validation process
             fails.
    :rtype: bool

    :raises Exception: If an error occurs at any point during the file sharing process, including issues with locating
                       the file, sharing operations, link generation, or access validations. The specific error message
                       is printed to provide insights into the encountered issue.

    **Example**::

        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> username = "example_user"
        >>> password = "password123"
        >>> file_name = "document.pdf"
        >>> share_success = share_file(driver, username, password, file_name)
        >>> if share_success:
        ...     print("File shared successfully.")
        ... else:
        ...     print("File sharing failed.")

    .. note::
        - This function assumes that the user initiating the share (typically an admin or the file owner) is
          logged into NextCloud at the start of the function.
        - The function performs a logout operation as part of its external link validation step, and then logs
          back in as the admin user. Ensure that any necessary session data is saved or that subsequent operations
          account for this logout/login cycle.
    """
    try:
    
    # Navigate to the file management page
        orange_text(f"Sharing file {file_name}...")
        ensure_logged_in_and_goto_files(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH, FILES_TAB_XPATH)
        
    # Find the file to share 

        locate_file_in_nextcloud(driver, file_name)
        

    # Click the share button
        locate_and_click_share_button(driver, file_name)
    # Check sharing file with another user
        share_file_with_recipient(driver,username, file_name, SHARE_WITH_ANOTHER_USER_INPUT_XPATH, SAVE_SHARING_BUTTON_XPATH)
        
    # Save both the internal and external share links in variables
        internal_share_link = get_internal_share_link(driver, INTERNAL_LINK_COPY_BUTTON_XPATH)
        print(f"Internal share link: {internal_share_link}")  
        external_share_link = get_external_share_link(driver, EXTERNAL_LINK_COPY_BUTTON_XPATH, EXTERNAL_LINK_COPY_BUTTON_XPATH_HREF)
        print(f"External share link: {external_share_link}")
        
   
        
        
    # Logout and navigate to external share link to check if it's accessible without being logged in
        logout_and_goto_external_link(driver, LOGOUT_BUTTON_PATH,LOGIN_BUTTON_XPATH,OPEN_SETTINGS_MENU_XPATH,CLOSED_SETTINGS_MENU_XPATH, external_share_link)
        check_external_file_sharing(driver, file_name)
        

    
    # Go to the share page using the internal share link to check if it's accessible without being logged in 
        check_internal_file_share(driver, file_name, internal_share_link, username, password, LOGIN_BUTTON_XPATH)
        

        
    # Logout and go back to Admin user to continue if there any other tests to run
        print("Deleting cookie")
        ifLogin_delete_cookies(driver)
        time.sleep(10)
        print("Logging in to Admin account from share_file function")
        login_to_nextcloud(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH)    
        return True    
    # Return True if the file is shared successfully, False otherwise
    except Exception as e:
        print(f"An error occurred during file sharing: {e}")
        return False    