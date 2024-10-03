
from functional_testing.utils.file_management import (
    ensure_logged_in_and_goto_files,
    perform_delete_file,
    orange_text
)
from functional_testing.config.configuration import (
    TARGET_URL, 
    USERNAME, 
    PASSWORD, 
    LOGIN_BUTTON_XPATH, 
    FILES_TAB_XPATH, 
)



def delete_file(driver, file_name):           
    """
    Deletes a specified file from NextCloud.

    This function navigates to the NextCloud files section by ensuring the session is logged in. It then attempts to
    delete a file with the given name. Successful deletion is verified internally by the function `perform_delete_file`.
    If the deletion process encounters any issues, an exception is raised.

    :param driver: An instance of Selenium WebDriver used for automating interactions with the NextCloud web
                   application. It should be properly initialized and configured prior to calling this function.
    :type driver: WebDriver
    :param file_name: The name of the file to be deleted from NextCloud. The name should match exactly with the file
                      present in NextCloud, including file extension.
    :type file_name: str

    :returns: True if the file is successfully deleted, False otherwise. This adjustment from the original docstring
              without a return statement provides clarity on the function's success through a boolean.
    :rtype: bool

    :raises AssertionError: If the file was not deleted successfully. This assertion could be raised within the
                            `perform_delete_file` function based on the verification of the file's absence after the
                            deletion attempt. Handling or logging this error in the calling context is recommended to
                            make informed workflow decisions based on the file deletion success.

    **Example**::

        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> file_name = "example_document.pdf"
        >>> deletion_success = delete_file(driver, file_name)
        >>> if deletion_success:
        ...     print(f"File {file_name} was successfully deleted.")
        ... else:
        ...     print(f"Failed to delete the file {file_name}.")

    """
    try:   
            orange_text(f"Deleting file {file_name}...")
            ensure_logged_in_and_goto_files(driver, TARGET_URL, USERNAME, PASSWORD, LOGIN_BUTTON_XPATH, FILES_TAB_XPATH)
            perform_delete_file(driver, file_name)
            return True
    except Exception as e:
        print(f"An error occurred during large size file deletion: {e}")
        return False