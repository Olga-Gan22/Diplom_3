import pytest
import allure
from utils.helpers import create_order_for_feed_tests


@allure.feature("Лента заказов")
@allure.description("Тесты ленты заказов: счётчики и раздел «В работе»")
class TestFeed:

    @allure.story("Счётчик «Выполнено за всё время»")
    @allure.title("Счётчик «Выполнено за всё время» увеличивается при новом заказе")
    @allure.description(
        "Проверяется, что после оформления нового заказа значение счётчика "
        "«Выполнено за всё время» на странице ленты заказов увеличивается."
    )
    def test_counter_total_increases(self, main_page, feed_page, logged_in_user):
        with allure.step("Открытие ленты и фиксация начального значения счётчика"):
            feed_page.open_feed()
            counter_before = feed_page.get_counter_total()

        with allure.step("Оформление нового заказа (через хелпер)"):
            create_order_for_feed_tests(main_page.driver)

        with allure.step("Повторное открытие ленты и проверка роста счётчика"):
            feed_page.open_feed()
            counter_after = feed_page.get_counter_total()

        assert counter_after > counter_before, (
            f"Счётчик «Выполнено за всё время» не увеличился: "
            f"было {counter_before}, стало {counter_after}"
        )

    @allure.story("Счётчик «Выполнено за сегодня»")
    @allure.title("Счётчик «Выполнено за сегодня» увеличивается при новом заказе")
    @allure.description(
        "Проверяется, что после оформления заказа значение счётчика "
        "«Выполнено за сегодня» увеличивается."
    )
    def test_counter_today_increases(self, main_page, feed_page, logged_in_user):
        with allure.step("Открытие ленты и фиксация начального значения"):
            feed_page.open_feed()
            counter_before = feed_page.get_counter_today()

        with allure.step("Оформление нового заказа (через хелпер)"):
            create_order_for_feed_tests(main_page.driver)

        with allure.step("Проверка роста счётчика «Выполнено за сегодня»"):
            feed_page.open_feed()
            counter_after = feed_page.get_counter_today()

        assert counter_after > counter_before, (
            f"Счётчик «Выполнено за сегодня» не увеличился: "
            f"было {counter_before}, стало {counter_after}"
        )

    @allure.story("Заказ в разделе «В работе»")
    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    @allure.description(
        "Проверяется, что оформленный заказ отображается в разделе «В работе» ленты. "
        "Тест запоминает номер заказа из модального окна подтверждения и ищет именно этот номер в списке."
    )
    def test_order_in_work(self, main_page, feed_page, logged_in_user):
        with allure.step("Оформление заказа и получение номера"):
            order_number = create_order_for_feed_tests(main_page.driver)
            assert order_number and order_number != "9999", (
                f"Не удалось получить номер заказа: {order_number}"
            )

        with allure.step("Переход в ленту и проверка наличия заказа"):
            feed_page.open_feed()

            assert feed_page.is_order_in_work(order_number), (
                f"Заказ №{order_number} не найден в разделе «В работе»"
            )
