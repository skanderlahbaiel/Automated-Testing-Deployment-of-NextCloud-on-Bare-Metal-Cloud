"""
This module defines configurations and locators for Selenium-based functional testing of the NextCloud application.

The configurations include paths, URLs, authentication details, file paths and sizes, base names and extensions for test files,
and XPath locators for various UI elements necessary for user management, file upload/download, and user session management.

Environment Variables:
    The module leverages environment variables to allow flexible configuration across different deployment environments.
    Users should set the following environment variables in their testing environment before executing tests:

    - `BASE_DIR`: The base directory path where created files and downloads during tests will be stored.
    - `CHROME_DRIVER_PATH`: The file system path to the ChromeDriver executable. Defaults to `/usr/bin/chromedriver` if not set.
    - `TARGET_URL`: The URL of the NextCloud instance to be tested. Example: 'https://nextcloud.example.com'
    - `USERNAME`: The username for authenticating with the NextCloud instance. Defaults to 'admin'.
    - `PASSWORD`: The password for the user. Example: 'password123'.
    - `FILE_SIZE_MEDIUM`: Specifies the size in mega Bytes of medium files in tests. Defaults to '1'.
    - `FILE_SIZE_LARGE`: Specifies the size in mega Bytes of large files in tests. Defaults to '1'.
    - `TEST_FILE_BASE_LARGE`: The base name for large test files. Defaults to 'test_large_file'.
    - `TEST_FILE_BASE_MEDIUM`: The base name for medium test files. Defaults to 'test_medium_file'.
    - `EXTENSION`: The file extension for test files. Defaults to '.txt'.

Setting Environment Variables
-----------------------------
Environment variables can be set in various ways depending on the operating system being used. This project contains a script that sets the environment variables for you. But if you want to set them manually, follow the instructions below:

Unix-like systems (Linux/macOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can export the variables in your shell before running the tests:

.. code-block:: bash

   export BASE_DIR=/path/to/base/dir
   export CHROME_DRIVER_PATH=/path/to/chromedriver
   export TARGET_URL=https://nextcloud.example.com
   export USERNAME=admin
   export PASSWORD=secret

Windows systems
^^^^^^^^^^^^^^^
You can set environment variables using the 'set' command in Command Prompt:

.. code-block:: bat

   set BASE_DIR=C:\\path\\to\\base\\dir
   set CHROME_DRIVER_PATH=C:\\path\\to\\chromedriver.exe
   set TARGET_URL=https://nextcloud.example.com
   set USERNAME=admin
   set PASSWORD=secret

Usage
-----
This module is intended to be imported and used in functional test scripts for NextCloud. The configurations and locators defined herein facilitate interaction with the NextCloud UI through Selenium WebDriver for various testing scenarios, such as user management, file operations, and session management.

Example usage in a test script:

.. code-block:: python

   from selenium import webdriver
   import functional_test_config as config

   driver = webdriver.Chrome(config.CHROME_DRIVER_PATH)
   driver.get(config.TARGET_URL)

.. note:: Ensure that the ChromeDriver version matches the version of Chrome installed on the testing system.

XPath Locators
--------------
This module defines several XPath locators for interacting with the NextCloud UI. These locators are used to find and interact with various buttons and other UI elements. These XPaths should work fine, until major updates in the NextCloud UI occur.

- `LOGIN_BUTTON_XPATH`: The XPath locator for the login button. Example: `'//input[@type="submit"]'`.
- `LOGOUT_BUTTON_XPATH`: The XPath locator for the logout button. Example: `'//a[@id="logout"]'`.
- `UPLOAD_BUTTON_XPATH`: The XPath locator for the file upload button. Example: `'//input[@type="file"]'`.
- `DELETE_BUTTON_XPATH`: The XPath locator for the delete file button. Example: `'//a[@class="action delete"]'`.

These XPath locators are used in conjunction with Selenium's `find_element_by_xpath` method to find and interact with the corresponding UI elements. For example:

.. code-block:: python

   login_button = driver.find_element_by_xpath(config.LOGIN_BUTTON_XPATH)
   login_button.click()

.. note:: The exact XPath locators will depend on the specific structure and styling of your NextCloud instance's UI. If the UI changes, these locators may need to be updated.
"""

import os

# Base directory for created files and downloads
BASE_DIR=os.getenv('BASE_DIR')

# Paths and URLs
CHROME_DRIVER_PATH=os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
TARGET_URL=os.getenv('TARGET_URL', 'http://skander-nextcloud.lijo')

# Authentication details
USERNAME=os.getenv('USERNAME', 'admin')
PASSWORD=os.getenv('PASSWORD', '?aymen!lijo!pass!')

# File paths
CREATED_FILES_PATH=os.path.join(BASE_DIR, "created_files")
DOWNLOAD_DIRECTORY=os.path.join(BASE_DIR, "downloads")

# File sizes
FILE_SIZE_MEDIUM=int(os.getenv('FILE_SIZE_MEDIUM', '1'))
FILE_SIZE_LARGE=int(os.getenv('FILE_SIZE_LARGE', '1'))


# User-changeable file base names and extension
TEST_FILE_BASE_LARGE=os.getenv('TEST_FILE_BASE_LARGE', "test_large_file")
TEST_FILE_BASE_MEDIUM=os.getenv('TEST_FILE_BASE_MEDIUM', "test_medium_file")
EXTENSION=os.getenv('EXTENSION', ".txt")

# Login/Logout button locators
LOGIN_BUTTON_XPATH="//button[@class='button-vue button-vue--icon-and-text button-vue--vue-primary button-vue--wide']"
OPEN_SETTINGS_MENU_XPATH="//a[@aria-label='Open settings menu' and @aria-expanded='true']"
CLOSED_SETTINGS_MENU_XPATH="//a[@aria-label='Open settings menu' and @aria-expanded='false']"
LOGOUT_BUTTON_PATH="//a[starts-with(@href, '/logout?')] | //a[contains(@href, '/logout?')] | //a[contains(@href, '/logout')] | //a[contains(text(), 'Log out')]"

# Upload download button locators
FILES_TAB_XPATH="//a[@aria-label='Files']"
NEW_FILE_OR_FOLDER_MENU_XPATH="//a[@class='button new' and @aria-label='New file/folder menu']"
FILE_UPLOAD_START_ID="file_upload_start"
FILE_UPLOAD_BUTTON_XPATH="//button[@class='button-vue button-vue--icon-and-text button-vue--vue-primary button-vue--wide']"

# Add user button locators
USERS_BUTTON_XPATH="//a[@href='/settings/users']"
NEW_USER_BUTTON="//button[@id='new-user-button']"
NEW_USERNAME_INPUT="//input[@id='newusername']"
NEW_DISPLAY_NAME_INPUT="//input[@id='newdisplayname']"
NEW_USER_PASSWORD_INPUT="//input[@id='newuserpassword']"
NEW_USER_EMAIL_INPUT="//input[@id='newemail']"
NEW_USER_GROUP_DROPDOWN="//div[@class='multiselect multiselect-vue multiselect--multiple']"
NEW_USER_ADMIN_GROUP="//span[@class='name-parts__first' and text()='admin']"
NEW_USER_QUOTA_DROPDOWN="//div[@class='quota modal__item']" 
NEW_USER_QUOTA_INPUT="//input[@placeholder='Select user quota']"


NEW_USER_MANAGERS_INPUT="//input[@placeholder='Select user manager']"
NEW_USER_MANAGERS_ADMIN="//li[@role='option' and contains(@class, 'multiselect__element')]//span[contains(@class, 'option') and @id='admin']"
NEW_USER_ADD_BUTTON="//button[@id='newsubmit']"
NEW_USER_FORM="//form[@id='new-user']"

NEW_USER_BUTTONS_XPATH = {
    "OPEN_SETTINGS_MENU_XPATH": OPEN_SETTINGS_MENU_XPATH,
    "USERS_BUTTON_XPATH": USERS_BUTTON_XPATH,
    "NEW_USER_BUTTON": NEW_USER_BUTTON,
    "NEW_USER_ADD_BUTTON": NEW_USER_ADD_BUTTON,
    "NEW_USER_QUOTA_DROPDOWN": NEW_USER_QUOTA_DROPDOWN,
    "NEW_USER_ADMIN_GROUP": NEW_USER_ADMIN_GROUP,
    "NEW_USER_MANAGERS_INPUT": NEW_USER_MANAGERS_INPUT,
    "NEW_USER_MANAGERS_ADMIN": NEW_USER_MANAGERS_ADMIN,
    "NEW_USER_QUOTA_INPUT": NEW_USER_QUOTA_INPUT,
    "NEW_USERNAME_INPUT": NEW_USERNAME_INPUT,
    "NEW_DISPLAY_NAME_INPUT": NEW_DISPLAY_NAME_INPUT,
    "NEW_USER_PASSWORD_INPUT": NEW_USER_PASSWORD_INPUT,
    "NEW_USER_EMAIL_INPUT": NEW_USER_EMAIL_INPUT,
    "NEW_USER_GROUP_DROPDOWN": NEW_USER_GROUP_DROPDOWN,
    "CLOSED_SETTINGS_MENU_XPATH": CLOSED_SETTINGS_MENU_XPATH,
}

# Delete user button locators
USER_ACTIONS_BUTTON_XPATH="//button[@aria-label='Toggle user actions menu']"
DELETE_USER_BUTTON_XPATH="//button[@class='menuitem focusable' and contains(text(), 'Delete user')]"
CONFIRM_DELETE_USER_BUTTON_XPATH="//button[@class='error primary']"


# Share locators
SHARE_BUTTON_XPATH="//a[@class='name']//a[@class='action action-share permanent']"
#INTERNAL_LINK_COPY_BUTTON_XPATH="//a[@aria-label='Copy internal link to clipboard']"
INTERNAL_LINK_COPY_BUTTON_XPATH = '/html/body/main/aside/div/div/section[1]/div/div[1]/ul[4]/li/a'

EXTERNAL_LINK_COPY_BUTTON_XPATH="//button[@aria-label='Create a new share link']"
EXTERNAL_LINK_COPY_BUTTON_XPATH_HREF = "/html/body/main/aside/div/div/section[1]/div/div[1]/ul[1]/li/div[2]/a"
SHARE_WITH_ANOTHER_USER_INPUT_XPATH="//input[@id='sharing-search-input']"
SAVE_SHARING_BUTTON_XPATH="//button[@type='button']//span[contains(text(), 'Save share')]"

# User modification locators
MODIFY_USER_BUTTON_XPATH="/html/body/div[3]/main/div/div[3]/div[8]/div[1]/button"
SAVE_MODIFICATION_BUTTON_XPATH="//button[@title='Done']"
