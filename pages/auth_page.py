import allure
from pages.base_page import BasePage
from pages.locators import AuthPageLocators
from config.urls import BASE_URL


@allure.feature("Авторизация и регистрация")
@allure.description("Страница регистрации и авторизации пользователя")
class AuthPage(BasePage):

    @allure.step("Регистрация пользователя: name={name}, email={email}")
    def register(self, name, email, password):
        self.open(f"{BASE_URL}register")
        self.send_keys(AuthPageLocators.INPUT_REG_NAME, name)
        self.send_keys(AuthPageLocators.INPUT_REG_EMAIL, email)
        self.send_keys(AuthPageLocators.INPUT_REG_PASSWORD, password)
        self.click_via_js(AuthPageLocators.BTN_REGISTER_SUBMIT)
        self.wait_url_contains("/login")

    @allure.step("Авторизация пользователя: email={email}")
    def login(self, email, password):
        self.send_keys(AuthPageLocators.INPUT_EMAIL, email)
        self.send_keys(AuthPageLocators.INPUT_PASSWORD, password)
        self.click_via_js(AuthPageLocators.BTN_SUBMIT_LOGIN)
        self.wait_url_not_contains("/login")
