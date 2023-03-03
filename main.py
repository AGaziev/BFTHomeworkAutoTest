import allure
import time

#from allure_commons.types import At...
from selenium import webdriver
from driverRep import DriverPath
from stepper import Stepper
from selenium.webdriver.common.by import By

driverPath = DriverPath.getDriverPath()

class TestGithubFeatures:
    def setup(self):
        self.driver = webdriver.Edge(driverPath)
        self.stepper = Stepper(self.driver)

    def teardown(self):
        self.driver.quit()

    @allure.story('Authentication to github')
    def login(self):


    @allure.feature('GitHub Features Test')
    def test_github_features(self):
        self.driver.get('https://github.com/login')
        self.login()

        self.findUser('VoiceDD')
        self.setStarToRep('')
