import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import allure
from functools import wraps


class Stepper:  # idk how to name this class
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step('Open {url}')
    def open_page(self, url):
        self.driver.get(url)

    @allure.step("Send {text} to {name}")
    def send_keys(self, elementInfo, by, text, name='element'):
        element, elementId = self.getElement(elementInfo, by)
        element.send_keys(text)

    @allure.step("Click {name}")
    def click(self, elementInfo, by, name='element'):
        element, elementId = self.getElement(elementInfo, by)
        element.click()

    @allure.step("Get {attributeName} from {name}")
    def getAttribute(self, elementInfo, by, attributeName, name='element'):
        element, elementId = self.getElement(elementInfo, by)
        return element.get_attribute(attributeName)

    def getElement(self, elementInfo, by):
        element = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((by,elementInfo)))
        try:
            elementId = element.id
        except:
            elementId = 'NoneId'
        return element, elementId
