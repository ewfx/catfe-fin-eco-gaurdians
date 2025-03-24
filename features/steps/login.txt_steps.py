
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

driver = None

def get_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@given('I open the application')
def step_open_browser(context):
    driver = get_driver()
    driver.get("http://localhost:3000/crud-app")

@then('Login using adminEmail admin@example.com and Password 12345 invalid credentials')
def step_then_1(context):
    
    driver.find_element(By.ID, 'email').send_keys('admin@example.com')
    driver.find_element(By.ID, 'password').send_keys('12345')
    driver.find_element(By.ID, 'login-button').click()

@then("I close the browser")
def step_close_browser(context):
    global driver
    if driver:
        driver.quit()
        driver = None
