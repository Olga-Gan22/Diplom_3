import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.main_page import MainPage
from pages.auth_page import AuthPage
from pages.feed_page import FeedPage
from utils.generators import get_user_data


@allure.feature("Фикстуры и управление браузером")
@allure.description("Настройка драйверов, параметризация браузеров, базовые страницы и авторизация")
def pytest_generate_tests(metafunc):
    """Параметризует фикстуру driver значениями chrome и firefox."""
    if "driver" in metafunc.fixturenames:
        metafunc.parametrize("driver", ["chrome", "firefox"], indirect=True)


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
# Фикстуры
# ------------------------------------------------------------

@pytest.fixture
@allure.description("Инициализирует браузер (Chrome/Firefox), разворачивает на весь экран, корректно закрывает после теста")
def driver(request):
    browser_name = request.param
    create_fn = BROWSERS[browser_name]

    with allure.step(f"Запуск браузера: {browser_name}"):
        driver = create_fn()
        driver.maximize_window()
        yield driver
        driver.quit()


@pytest.fixture
@allure.description("Открывает главную страницу и ждёт её полной загрузки")
def main_page(driver):
    page = MainPage(driver)
    with allure.step("Открытие главной страницы и ожидание загрузки"):
        page.open_main_page()
        page.wait_page_loaded()
    return page


@pytest.fixture
@allure.description("Создаёт экземпляр страницы авторизации")
def auth_page(driver):
    return AuthPage(driver)


@pytest.fixture
@allure.description("Создаёт экземпляр страницы ленты заказов")
def feed_page(driver):
    return FeedPage(driver)


@pytest.fixture
@allure.description("Генерирует уникальные тестовые данные пользователя (name, email, password)")
def registered_user():
    return get_user_data()


@pytest.fixture
@allure.description("Регистрирует и авторизует пользователя, возвращает данные пользователя")
def logged_in_user(auth_page, registered_user):
    with allure.step("Регистрация нового пользователя"):
        auth_page.register(
            registered_user["name"],
            registered_user["email"],
            registered_user["password"],
        )

    with allure.step("Авторизация пользователя"):
        auth_page.login(
            registered_user["email"],
            registered_user["password"],
        )

    return registered_user
