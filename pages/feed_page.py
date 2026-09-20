import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators import FeedPageLocators
from config.urls import FEED_PAGE_URL
from helpers import wait_for_order_in_work


class FeedPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открытие страницы «Лента заказов»")
    def open_feed(self):
        self.driver.get(FEED_PAGE_URL)
        self.wait.until(
            EC.visibility_of_element_located(FeedPageLocators.FEED_TITLE)
        )

    @allure.step("Получение значения счётчика «Выполнено за всё время»")
    def get_counter_total(self):
        el = self.wait.until(
            EC.visibility_of_element_located(FeedPageLocators.COUNTER_TOTAL)
        )
        return int(el.text)

    @allure.step("Получение значения счётчика «Выполнено за сегодня»")
    def get_counter_today(self):
        el = self.wait.until(
            EC.visibility_of_element_located(FeedPageLocators.COUNTER_TODAY)
        )
        return int(el.text)

    @allure.step("Проверка появления заказа в разделе «В работе»")
    def is_order_in_work(self, timeout=15):
        wait_for_order_in_work(self.driver, timeout)
        return True
