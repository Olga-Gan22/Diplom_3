import allure
import re
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from pages.locators import FeedPageLocators
from config.urls import FEED_URL


@allure.feature("Лента заказов")
@allure.description("Страница ленты заказов: счётчики и раздел «В работе»")
class FeedPage(BasePage):

    @allure.step("Открытие страницы «Лента заказов»")
    def open_feed(self):
        self.open(FEED_URL)
        self.find(FeedPageLocators.FEED_TITLE)

    @allure.step("Получение значения счётчика «Выполнено за всё время»")
    def get_counter_total(self):
        text = self.find(FeedPageLocators.COUNTER_TOTAL).text
        return int(re.sub(r"\D", "", text))

    @allure.step("Получение значения счётчика «Выполнено за сегодня»")
    def get_counter_today(self):
        text = self.find(FeedPageLocators.COUNTER_TODAY).text
        return int(re.sub(r"\D", "", text))

    @allure.step("Проверка, что заказ №{order_number} отображается в разделе «В работе»")
    def is_order_in_work(self, order_number, timeout=30):
        target_number = f"0{order_number}"

        def order_appeared(_driver):
            items = self.find_all(FeedPageLocators.WORK_LIST_ITEM)
            return any(item.text.strip() == target_number for item in items)

        WebDriverWait(self.driver, timeout).until(order_appeared)
        return True
