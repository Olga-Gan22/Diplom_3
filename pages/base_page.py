import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Базовая страница")
@allure.description("Базовый класс для всех страниц: поиск, клики, ожидания, работа с драйвером")
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Поиск элемента: {locator}")
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Поиск всех элементов: {locator}")
    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Ожидание кликабельности элемента: {locator}")
    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        self.wait_clickable(locator).click()

    @allure.step("Ввод текста в поле: {locator}")
    def send_keys(self, locator, text):
        el = self.wait_clickable(locator)
        el.clear()
        el.send_keys(text)

    @allure.step("Получение текста элемента: {locator}")
    def get_text(self, locator):
        return self.find(locator).text

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Ожидание, что URL содержит: {url_part}")
    def wait_url_contains(self, url_part):
        self.wait.until(lambda d: url_part in d.current_url)

    @allure.step("Ожидание, что URL НЕ содержит: {url_part}")
    def wait_url_not_contains(self, url_part):
        self.wait.until(lambda d: url_part not in d.current_url)

    @allure.step("Открытие страницы: {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Скролл к элементу: {locator}")
    def scroll_to(self, locator):
        el = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", el)

    @allure.step("Выполнение JavaScript-скрипта")
    def execute_script(self, script, *args):
        self.driver.execute_script(script, *args)

    @allure.step("Проверка, что элемент присутствует на странице: {locator}")
    def is_element_present(self, locator):
        return bool(self.driver.find_elements(*locator))

    @allure.step("Удалить модальный оверлей из DOM")
    def close_modal_overlay(self):
        self.driver.execute_script(
            "document.querySelectorAll('.Modal_modal_overlay__x2ZCr').forEach(el => el.remove());"
        )

    @allure.step("Клик по элементу через JavaScript")
    def click_via_js(self, locator):
        element = self.wait_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ожидание, что элемент невидим: {locator}")
    def wait_invisible(self, locator):
        """Ждёт, пока элемент станет невидимым или исчезнет из DOM"""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Ожидание выполнения условия: {condition_name}")
    def wait_until(self, condition, condition_name="условие"):
        """Универсальное ожидание по кастомному условию"""
        return self.wait.until(condition)
