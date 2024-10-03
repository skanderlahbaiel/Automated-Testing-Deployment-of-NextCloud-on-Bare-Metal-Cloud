## 1. Install Allure

a. Go to the [latest Allure Report release on GitHub](https://github.com/allure-framework/allure2/releases/tag/2.27.0) and download the allure-*.deb or allure-*.rpm package, depending on which package format your Linux distribution supports.

b. In a terminal, go to the directory with package and install it.

For the DEB package:

```
    sudo dpkg -i allure_2.24.0-1_all.deb
```
For the RPM package:

```
    sudo rpm -i allure_2.24.0-1.noarch.rpm
```

## 2. Install the packages from requirements.txt

To install the requirements:

````
    pip install requirements.txt
````
## 3. Configuration variables for functional testing

#### The path to the ChromeDriver executable.
`CHROME_DRIVER_PATH`: str = "/path/to/chromedriver"

#### The URL of the NextCloud website.
`TARGET_URL`: str = "https://example.com"

#### The username for authentication.
`USERNAME`: str = "your_username"

#### The password for authentication.
`PASSWORD`: str = "your_password"

#### The path to the directory where created files will be stored.
`CREATED_FILES_PATH`: str = "/path/to/created/files"

#### The size of a medium file.
`FILE_SIZE_MEDIUM`: int = 10

#### The size of a large file.
`FILE_SIZE_LARGE`: int = 100

#### The path to the directory where downloaded files will be saved.
`DOWNLOADS_PATH`: str = "/path/to/downloaded/files"








## 4. Run the Test Using Pytest & Allure

Ensure that you use pytest to run the tests and generate Allure results. To run the test suite:

```
    pytest -s --alluredir=./test_results upload_file.py
```



## 5. Generate the Allure Report

To generate Allure report:

```
    allure serve ./rest_results
```

How to run the script:

Set the environment variables in your shell before running the script:

export USERNAME="your_username"
export PASSWORD="your_password"
./your_script.sh