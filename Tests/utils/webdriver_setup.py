from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from functional_testing.config.configuration import (
    CHROME_DRIVER_PATH,  
    DOWNLOAD_DIRECTORY, 
)

def driver():
    """
    Creates and returns a new instance of the Chrome WebDriver.

    Returns:
        WebDriver: The Chrome WebDriver instance.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Remote debugging port is optional for local running and seeing things happening
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIRECTORY,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    # Setting up the Chrome WebDriver instance, it allows to interact with the browser
    service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
    # Creating a new instance of the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
  
    # Maximizing the window and setting the zoom level to 100%, to ensure all elements are visible
    driver.maximize_window()
    return driver