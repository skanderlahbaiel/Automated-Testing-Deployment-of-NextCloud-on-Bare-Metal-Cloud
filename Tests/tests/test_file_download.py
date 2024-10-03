from functional_testing.utils.file_management import (
    perform_download_file,
    ensure_logged_in_and_goto_files,
)
from functional_testing.config.configuration import (
    TARGET_URL, 
    USERNAME, 
    PASSWORD, 
    LOGIN_BUTTON_XPATH, 
    FILES_TAB_XPATH,  
    DOWNLOAD_DIRECTORY, 
)



def download_file(driver, file_name):
    """
    Downloads a specified file from NextCloud.

    This function first ensures that the session is logged into NextCloud, and that the file management screen is open, by invoking `ensure_logged_in_and_goto_files`.
    It then attempts to download a file with the specified `file_name`. The success of the download operation is
    determined by checking the presence of the downloaded file in a predetermined download directory. This function
    assumes that `perform_download_file` is responsible for both downloading the file and verifying its presence
    in the `DOWNLOAD_DIRECTORY`.

    :param driver: An instance of Selenium WebDriver, used for automating interactions with the web
                   application. The driver should be configured to handle file downloads, including
                   specifying the download directory.
    :type driver: WebDriver
    :param file_name: The name of the file to be downloaded from NextCloud. The file name should include any
                      file extension if applicable and match exactly with a file available in NextCloud.
    :type file_name: str
    :return: True if the file is successfully downloaded and verified to be present in the local download
             directory, False otherwise.
    :rtype: bool
    :raises Exception: If any error occurs during the process of navigating to the files page, initiating the file
                       download, or verifying the file's presence in the local directory.

    .. note:: 
        - The function leverages configuration variables from `functional_testing.config.configuration` for navigation
          and login. 
        - The download directory is set via the `DOWNLOAD_DIRECTORY` configuration variable. This directory should
          be correctly configured in both the WebDriver setup and the environment to ensure downloaded files are
          saved and found as expected.
        - The function prints a success message in green upon successful download. This visual cue can be helpful in
          interactive or manual testing scenarios.

    .. code-block:: python

        from selenium import webdriver
        driver = webdriver.Chrome()
        file_name = "sample_document.pdf"
        success = download_file(driver, file_name)
        if success:
            print(f"The file {file_name} was successfully downloaded.")
        else:
            print(f"Failed to download the file {file_name}.")
    """
    try:
        # Ensure the user is logged in and navigate to the files tab
        ensure_logged_in_and_goto_files(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH, FILES_TAB_XPATH)
        # Download the file from NextCloud and check if it is found in the local directory
        perform_download_file(driver, file_name, DOWNLOAD_DIRECTORY)
        print("\033[92mFile download test passed and the file was found in the local directory\033[0m")  # Print in green
        return True
    except Exception as e:
        print(f"An error occurred during file download: {e}")
        return False
    

