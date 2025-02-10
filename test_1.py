import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sauceclient import SauceClient
import os
import sys

def teardown(quit_msg, exception):
    print(f"{quit_msg}\n", exception)
    driver.quit()
    sys.exit(1)

username = os.environ.get('SAUCE_USERNAME')
access_key = os.environ.get('SAUCE_ACCESS_KEY')
sauce_client = SauceClient(username, access_key)
options = ChromeOptions()
options.platform_name = 'macOS 13'
options.browser_version = 'latest'

sauce_options = {
    'name': f'Running test on {options.platform_name}',
    'build': 'Build For Kadir',
    'extendedDebugging' : True,
   ## 'prerun': {
     ##   "executable": "https://raw.githubusercontent.com/kadir-sauce/sl/refs/heads/main/test.sh",
  #  }
}


options.set_capability('sauce:options', sauce_options)

def wait_for_visibility_of_element_id(driver_instance, xpath):
    try:
        elem = WebDriverWait(driver_instance, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        elem = False
    return elem

@pytest.fixture
def driver():
    driver = webdriver.Remote(
        command_executor=f"http://{username}:{access_key}@ondemand.eu-central-1.saucelabs.com/wd/hub",
        options=options
    )
    driver.maximize_window()

    yield driver
    driver.quit()

def test_dynamic_loading(driver):
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    driver.find_element(By.XPATH,value='//*[@id="start"]/button').click()

    #wait_for_visibility_of_element_id(driver, 'start').click()
    wait_for_visibility_of_element_id(driver,'//*[@id="finish"]')
    #el=driver.find_element(By.XPATH,value='//*[@id="finish"]/h4').text
    print(driver.find_element(By.XPATH,value='//*[@id="finish"]/h4').text)
    assert "Hello World" in driver.find_element(By.XPATH,value='//*[@id="finish"]/h4').text
