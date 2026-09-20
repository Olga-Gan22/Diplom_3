import allure
import uuid
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.main_page import MainPage
from pages.auth_page import AuthPage
from pages.feed_page import FeedPage


# ------------------------------------------------------------
# Фабрика драйверов
# ------------------------------------------------------------

def _create_chrome():
    options = webdriver.ChromeOptions()
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _create_firefox():
    options = webdriver.FirefoxOptions()
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


BROWSERS = {
    "chrome": _create_chrome,
    "firefox": _create_firefox,
}


# ------------------------------------------------------------
# Параметризация браузеров
# ------------------------------------------------------------

def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        metafunc.parametrize("driver", ["chrome", "firefox"], indirect=True)


# ------------------------------------------------------------
# Фикстуры (с with allure.step для логирования действий)
# ------------------------------------------------------------

@pytest.fixture
def driver(request):
    browser_name = request.param
    create_fn = BROWSERS[browser_name]
    
    with allure.step(f"Запуск браузера: {browser_name}"):
        driver = create_fn()
        driver.maximize_window()
        yield driver
        driver.quit()


@pytest.fixture
def main_page(driver):
    page = MainPage(driver)
    with allure.step("Открытие главной страницы и ожидание загрузки"):
        page.open_main_page()
        page.wait_page_loaded()
    return page


@pytest.fixture
def registered_user():
    """Генерирует уникальные данные для регистрации пользователя."""
    return {
        "name": "TestUser",
        "email": f"test_{uuid.uuid4().hex[:8]}@yandex.ru",
        "password": "123456",
    }


@pytest.fixture
def auth_page(driver, registered_user):
    auth = AuthPage(driver)
    
    with allure.step("Регистрация нового пользователя"):
        auth.register(
            registered_user["name"],
            registered_user["email"],
            registered_user["password"],
        )
    
    with allure.step("Авторизация пользователя"):
        auth.login(
            registered_user["email"],
            registered_user["password"],
        )
    
    return auth


@pytest.fixture
def feed_main_page(driver, auth_page):
    page = MainPage(driver)
    with allure.step("Переход на главную страницу и ожидание загрузки (для тестов ленты)"):
        page.open_main_page()
        page.wait_page_loaded()
    return page


@pytest.fixture
def feed_page(driver, auth_page):
    return FeedPage(driver)
