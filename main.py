import allure
import time

# from allure_commons.types import At...
from selenium import webdriver
# from driverRep import DriverPath
from stepper import Stepper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driverPath = r'drivers\driver.exe'  # DriverPath.getDriverPath()


class TestGithubFeatures:
    login = 'adminGithuba'
    password = 'hardpass999'
    profileUsernameToFind = 'VoiceDD'
    testRepo = 'BFTHomeworkAutoTest'

    def setup(self):
        self.driver = webdriver.Edge(driverPath)
        self.driver.maximize_window()
        self.stepper = Stepper(self.driver)

    def teardown(self):
        self.driver.quit()

    @allure.step('Waiting for DOM loaded')
    def wait(self, sec=1):
        time.sleep(sec)

    @allure.feature("Test Github Features")
    @allure.story('Authentication to github')
    def test_login(self):
        self.stepper.open_page('https://github.com/login')
        self.stepper.send_keys('login_field',
                               By.ID, self.login, name='login field')
        self.stepper.send_keys('password',
                               By.ID, self.password, name='password field')
        self.stepper.click('/html/body/div[1]/div[3]/main/div/div[4]/form/div/input[11]',
                           By.XPATH, name='Sign in button')
        with allure.step('Check current URL is main page'):
            assert self.driver.current_url == 'https://github.com/'
        self.checkUser(self.login)
        self.driver.refresh()  # bc need to close user panel features menu (otherwise intercepted)

    @allure.step('Check user {username} on main page')
    def checkUser(self, username):
        self.stepper.click('/html/body/div[1]/div[1]/header/div[7]/details/summary',
                           By.XPATH, 'profile features container')
        actualUsername = self.stepper.getAttribute(
            '/html/body/div[1]/div[1]/header/div[7]/details/details-menu/div[1]/a',
            By.XPATH, 'text', name='textbox contains username')
        actualUsername = actualUsername.removeprefix('Signed in as ')
        assert actualUsername == username

    @allure.feature("Test Github Features")
    @allure.story('Finding user profile by search')
    def test_find_user(self):
        with allure.step('Login'):
            self.test_login()
        with allure.step('Start search by username'):
            self.stepper.send_keys('/html/body/div[1]/div[1]/header/div[3]/div/div/form/label/input[1]',
                                   By.XPATH, self.profileUsernameToFind, 'search')
            self.stepper.click('jump-to-suggestion-search-global',
                               By.ID, 'Search All Github')
            self.stepper.click('/html/body/div[1]/div[6]/main/div/div[2]/nav[1]/a[10]',
                               By.XPATH, 'User Filter')
            self.stepper.click(f'//*[@id="user_search_results"]/div//a[contains(em, "{self.profileUsernameToFind}")]',
                               By.XPATH, "User Card in results")
        with allure.step("Star a test repository"):
            self.stepper.click(
                f'//*[@id="user-profile-frame"]/div/div[1]/div/ol//li//a[contains(span,"{self.testRepo}")]',
                By.XPATH, "test repository card")
            starCountBefore = int(self.stepper.getAttribute(
                '//*[@id="repo-content-pjax-container"]/div/div/div[2]/div[2]/div/div[1]/div/div[2]/a/strong',
                By.XPATH, 'innerText', 'star count'))
            self.stepper.click(
                '/html/body/div[1]/div[6]/div/main/div/div[1]/ul/li[3]/div/div[2]/form/button',
                By.XPATH, 'star button')
            time.sleep(1)  # wait until star info refreshing on server
            self.driver.refresh()
            starCountAfter = int(self.stepper.getAttribute(
                '//*[@id="repo-content-pjax-container"]/div/div/div[2]/div[2]/div/div[1]/div/div[2]/a/strong',
                By.XPATH, 'innerText', 'star count'))
        with allure.step("Star comparison test"):
            assert starCountAfter - starCountBefore == 1

    def test_logout(self):
        with allure.step('Login'):
            self.test_login()
        with allure.step('Logout'):
            self.stepper.click('/html/body/div[1]/div[1]/header/div[7]/details/summary',
                               By.XPATH, 'profile features container')
            self.stepper.click('/html/body/div[1]/div[1]/header/div[7]/details/details-menu/form/button',
                               By.XPATH, 'Sign out button')
        with allure.step('Check logout completed'):
            signIn = self.stepper.getAttribute('/html/body/div[1]/div[1]/header/div/div[2]/div/div/div[2]/a',
                                               By.XPATH, 'innerText', 'Sign in button')
            assert signIn == 'Sign in'
