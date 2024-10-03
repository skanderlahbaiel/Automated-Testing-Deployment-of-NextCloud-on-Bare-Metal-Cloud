"""
Automated Test Sequence for File and User Management Functionalities
---------------------------------------------------------------------

This automated test script is designed to validate the comprehensive functionalities related to file and user management within a web application environment. It executes a series of operations to test the system's ability to handle user and file lifecycle processes, such as adding and removing users, uploading, downloading, sharing files, and verifying file integrity, within a single, continuous execution flow.

.. note::
   This script is intended to be executed indirectly via the ``setup.sh`` shell script after all necessary environment variables have been configured. It is an example of how the test modules can be utilized in a real-world scenario, demonstrating the critical nature of the tested functionalities.\n
   The test script follows a predetermined sequence of steps `explained below` to simulate realistic application usage scenarios. The steps are encapsulated in a function. 


Execution Context
^^^^^^^^^^^^^^^^^
- **Not for Direct Execution**: This script is executed as part of the ``setup.sh`` script, which prepares the environment and triggers this test sequence.
- **Environment Configuration**: Necessary environment variables and application settings must be configured prior to execution.

Example Usage
-------------
This script is not intended for direct call. It is automatically executed, after setting up all environment variables through ``setup.sh``:

.. code-block:: bash

    ./setup.sh `'username'` `'password'` # This script indirectly executes the Python test script.

.. note::
   - The test utilizes pytest fixtures for setting up the driver and test files.
   - Detailed error messages are generated for failures, facilitating quick identification and remediation of issues encountered during testing.

The stringent test sequence and its execution context highlight the script's role in ensuring the application's operational integrity and reliability.
"""


import pytest, time
from functional_testing.tests.test_login import login
from functional_testing.utils.webdriver_setup import driver as setup_driver
from functional_testing.tests.test_file_upload import upload_file
from functional_testing.tests.test_file_download import download_file
from functional_testing.tests.test_file_integrity import file_integrity
from functional_testing.tests.test_file_delete import delete_file
from functional_testing.tests.test_logout import logout
from functional_testing.tests.test_create_user import add_user
from functional_testing.tests.test_delete_user import delete_user
from functional_testing.tests.test_file_share import share_file
from functional_testing.tests.test_modify_quota import modify_user_quota

from functional_testing.utils.file_management import (
    create_testing_files,    
)
from functional_testing.utils.user_management import (
    generate_user,
)
from functional_testing.config.configuration import (
    CREATED_FILES_PATH, # Create a medium size file
    FILE_SIZE_MEDIUM, 
    FILE_SIZE_LARGE, 
    TEST_FILE_BASE_LARGE,
    TEST_FILE_BASE_MEDIUM,
    EXTENSION,
)



@pytest.fixture(scope="session")
def test_files():
    """
    Pytest fixture that creates and returns paths and names of medium and large size test files.

    This fixture uses the `create_testing_files` function to create medium and large size test files. 
    The paths and names of these files are then returned for use in other test functions.

    The fixture has a session scope, which means it's invoked once per test session. 
    The created files can be used across multiple test functions in the test session.

    :return: A tuple containing the paths and names of the medium and large size test files. 
             The tuple is structured as follows: 
             (medium_size_file_path, medium_size_file_name, large_size_file_path, large_size_file_name)

    :rtype: tuple
    """
    medium_size_file_path, medium_size_file_name, large_size_file_path, large_size_file_name = create_testing_files(
        FILE_SIZE_MEDIUM, FILE_SIZE_LARGE, CREATED_FILES_PATH, TEST_FILE_BASE_MEDIUM, TEST_FILE_BASE_LARGE, EXTENSION
    )
    return medium_size_file_path, medium_size_file_name, large_size_file_path, large_size_file_name

@pytest.fixture(scope="session")
def driver():
    """
    Pytest fixture that sets up and tears down a webdriver session.

    This fixture uses the `setup_driver` function to initialize a webdriver session. 
    The driver object is then yielded for use in other test functions.

    After all tests have finished using the driver, the `driver.quit` method is called to 
    close the browser and end the webdriver session.

    The fixture has a session scope, which means it's invoked once per test session. 
    The same driver object can be used across multiple test functions in the test session.

    :return: A webdriver object for interacting with the browser.
    :rtype: webdriver object
    """
    driver = setup_driver()
    yield driver
    driver.quit

@pytest.mark.usefixtures("test_files")
def test_file_management_cycle(driver, test_files):
    """
    Test the file management cycle: upload, download, check integrity, share, delete.

    This function tests the entire file management cycle in a sequential manner. It includes the following steps:\n
    
    Workflow
    ^^^^^^^^

    1. **Login**
    2. **Add a User**
    3. **Upload Medium and Large Files**
    4. **Download Files**
    5. **Verify File Integrity**
    6. **Share File**
    7. **Delete Files**
    8. **Delete User**
    9. **Logout**
    
    .. warning::
       If any step in this sequence fails, the entire test is considered failed and an assertion error is raised with a relevant error message. This strict pass/fail criteria ensure the application's critical functionalities are robustly validated. The interdependency of test steps highlights the integrated nature of the application's functionalities.

    :param driver: A webdriver object for interacting with the browser.
    :type driver: webdriver object
    :param test_files: A tuple containing the paths and names of the medium and large size test files.
    :type test_files: tuple
    """
    medium_size_file_path, medium_size_file_name, large_size_file_path, large_size_file_name = test_files
            # Generate user details
    username, display_name, password, email, group, quota, manager = generate_user(group='admin', quota='1 GB', manager='admin')
    try:
        # Login 
        login_value =login(driver)
        assert login_value, "Login failed"
        
       
        
        # Add a user
        added_user_value = add_user(driver, username, display_name, password, email, group, quota, manager)
        assert added_user_value, "User addition failed"
        
        # Modify the user quota
        modified_quota_value = modify_user_quota(driver, username, quota='2 GB', password=password)
        assert modified_quota_value, "User quota modification failed"
        
        # Upload the medium size file
        
        upload_medium = upload_file(driver, medium_size_file_path)
        assert upload_medium, "Medium size file upload failed"
        
        # Upload the large size file
        upload_large = upload_file(driver, large_size_file_path)
        assert upload_large, "Large size file upload failed"
        

        
        # Download the medium size file
        download_medium = download_file(driver, medium_size_file_name)
        assert download_medium, "Medium size file download failed"
        
        # Download the large size file
        download_large = download_file(driver, large_size_file_name)
        assert download_large, "Large size file download failed"
        
        # Check the integrity of the medium size file
        integrity_medium = file_integrity(medium_size_file_name)
        assert integrity_medium, "Medium size file integrity check failed"
        
        # Check the integrity of the large size file
        integrity_large = file_integrity(large_size_file_name)
        assert integrity_large, "Medium size file integrity check failed"
        
        # Share the medium size file
        # Sharing the file with the user is not enough, 
        # we do login as the user and check if the file is shared with the user
        shared_file_value = share_file(driver, username, password, medium_size_file_name)
        assert shared_file_value, "File sharing failed"
        
        
        
        # Delete the medium size file
        delete_medium = delete_file(driver, medium_size_file_name)
        assert delete_medium, "Medium size file deletion failed"
        
        # Delete the large size file 
        delete_large = delete_file(driver, large_size_file_name)
        assert delete_large, "Medium size file deletion failed"
        
        deleted_user_value = delete_user(driver, username)
        assert deleted_user_value, "User deletion failed"
        

        

        
        logout_value = logout(driver)
        assert logout_value, "Logout failed"
        
    except Exception as e:
        print(f"An error occurred during the file management cycle: {e}")
        pytest.fail()
    
