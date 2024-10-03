from selenium.common.exceptions import TimeoutException
from functional_testing.utils.file_management import (
    perform_file_upload, 
    check_file_presence,
    toggle_file_upload,
    click_new_fileOrFolder,
    ensure_logged_in_and_goto_files,
    orange_text
)
from functional_testing.config.configuration import (
    TARGET_URL, 
    USERNAME, 
    PASSWORD, 
    LOGIN_BUTTON_XPATH, 
    FILES_TAB_XPATH, 
    NEW_FILE_OR_FOLDER_MENU_XPATH, 
    FILE_UPLOAD_START_ID, 
)


def upload_file(driver, file_path):
    """
    Uploads a file to NextCloud and verifies its presence in the file list in Nextcloud UI.

    This function automates the process of uploading a file to NextCloud using Selenium WebDriver. It ensures that
    the user is logged in and navigates to the files section. The function then initiates the file upload process and
    verifies whether the uploaded file appears in NextCloud's file list. If the file is not found within a specified
    timeout, the upload is considered unsuccessful.

    :param driver: The Selenium WebDriver instance used to automate browser interactions. It should be
                   initialized and configured to the target NextCloud instance prior to calling this function.
    :type driver: WebDriver
    :param file_path: The absolute path of the file on the local system that is to be uploaded. Ensure that the
                      path is accessible and readable by the script to avoid errors during the upload process.
    :type file_path: str
    :return: True if the file is successfully uploaded and verified to be present in NextCloud's file list.
             False if the file does not appear in the list after the upload process, indicating a failure.
    :rtype: bool
    :raises Exception: General exception if an error occurs at any point during the login, navigation, upload process,
                       or file presence check. The specific exception message is printed to provide insights into the
                       failure reason.

    .. note:: 
        - This function assumes that `TARGET_URL`, `USERNAME`, `PASSWORD`, `LOGIN_BUTTON_XPATH`, `FILES_TAB_XPATH`,
          `NEW_FILE_OR_FOLDER_MENU_XPATH`, and `FILE_UPLOAD_START_ID` are correctly configured in the
          `functional_testing.config.configuration` module.
        - Ensure that the WebDriver instance (`driver`) has been correctly authenticated with NextCloud prior to
          calling this function if not relying on the function's login mechanism. It's recommended to use the login function before calling this function.

    .. code-block:: python

        from selenium import webdriver
        driver = webdriver.Chrome()
        file_path = "/path/to/your/file.txt"
        upload_success = upload_file(driver, file_path)
        if upload_success:
            print("File upload successful.")
        else:
            print("File upload failed.")
    """
    try:    
            orange_text(f"Uploading file {file_path}...")
            ensure_logged_in_and_goto_files(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH, FILES_TAB_XPATH)
            toggle_file_upload(driver, FILE_UPLOAD_START_ID)
            # Upload the file and get the XPath of the uploaded file
            file_xpath = perform_file_upload(driver, file_path, FILE_UPLOAD_START_ID)
            try:
                # Checks the appearance of the uploaded file name in the NextCloud file list
                check_file_presence(driver, file_xpath, 120)
                file_found = True
            except TimeoutException:
                print("\033[92mFile not found in NextCloud, upload test failed\033[0m")
                file_found = False

            assert file_found, "The uploaded file was not found in NextCloud"
            print("\033[92mFile found in NextCloud, upload test passed!\033[0m")
            # Close the action menu
            click_new_fileOrFolder(driver, NEW_FILE_OR_FOLDER_MENU_XPATH)
            return True

    except Exception as e:
        # Print error message if upload fails
        print(f"An error occurred during file upload: {e}")
        return False



