import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators import AuthPageLocators
from config.urls import BASE_URL


class AuthPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Регистрация пользователя: name={name}, email={email}")
    def register(self, name, email, password):
        self.driver.get(f"{BASE_URL}register")

        name_field = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.INPUT_REG_NAME)
        )
        name_field.send_keys(name)

        email_field = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.INPUT_REG_EMAIL)
        )
        email_field.send_keys(email)

        password_field = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.INPUT_REG_PASSWORD)
        )
        password_field.send_keys(password)

        btn = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.BTN_REGISTER_SUBMIT)
        )
        btn.click()

        self.wait.until(lambda d: "/login" in d.current_url)

    @allure.step("Авторизация пользователя: email={email}")
    def login(self, email, password):
        email_field = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.INPUT_EMAIL)
        )
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.INPUT_PASSWORD)
        )
        password_field.clear()
        password_field.send_keys(password)

        btn = self.wait.until(
            EC.element_to_be_clickable(AuthPageLocators.BTN_SUBMIT_LOGIN)
        )
        btn.click()

        self.wait.until(lambda d: "/login" not in d.current_url)
