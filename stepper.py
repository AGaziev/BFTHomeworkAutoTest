from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import allure

class Stepper: # idk how to name this class
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step('Open {url}')
    def open_page(self, url):
        self.driver.get(url)

    @allure.step("Send text {text} to {elementId}")
    def send_keys(self, elementInfo, text, by):
        element, elementId = self.getElement(by, elementInfo)
        element.send_keys(text)

    @allure.step("Click {elementId}")
    def click(self, elementInfo, by):
        element, elementId = self.getElement(by, elementInfo)
        element.click()

    @allure.step("Get {attributeName} from {elementId}")
    def getAttribute(self, elementInfo, attributeName, by):
        element, elementId = self.getElement(by, elementInfo)
        return element.get_attribute(attributeName)

    def getElement(self, by, elementInfo):
        element = self.driver.find_element(by, elementInfo)
        elementId = element.get_attribute('id')
        return element, elementId