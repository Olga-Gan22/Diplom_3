import time
import pytest
import allure


@allure.feature("Лента заказов")
class TestFeed:

    @allure.story("Счётчик «Выполнено за всё время»")
    @allure.title("Счётчик «Выполнено за всё время» увеличивается при новом заказе")
    @allure.description(
        "Проверяется, что после оформления нового заказа значение счётчика "
        "«Выполнено за всё время» на странице ленты заказов увеличивается. "
        "Тест фиксирует значение до, оформляет заказ, затем проверяет рост счётчика."
    )
    def test_counter_total_increases(self, feed_main_page, feed_page):
        with allure.step("Открытие ленты заказов и получение начального значения счётчика"):
            feed_page.open_feed()
            counter_before = feed_page.get_counter_total()

        with allure.step("Оформление нового заказа на главной странице"):
            feed_main_page.open_main_page()
            feed_main_page.wait_page_loaded()
            feed_main_page.add_ingredient_to_order("Краторная булка N-200i")
            feed_main_page.add_ingredient_to_order("Соус Spicy-X")
            feed_main_page.submit_order()
            feed_main_page.close_order_modal()

        with allure.step("Повторное открытие ленты и проверка увеличения счётчика"):
            feed_page.open_feed()
            counter_after = feed_page.get_counter_total()

        assert counter_after > counter_before, (
            f"Счётчик «Выполнено за всё время» не увеличился: "
            f"было {counter_before}, стало {counter_after}"
        )

    @allure.story("Счётчик «Выполнено за сегодня»")
    @allure.title("Счётчик «Выполнено за сегодня» увеличивается при новом заказе")
    @allure.description(
        "Проверяется корректность работы счётчика «Выполнено за сегодня»: "
        "после создания заказа значение должно увеличиться. Тест фиксирует начальное "
        "значение, оформляет заказ и подтверждает рост показателя."
    )
    def test_counter_today_increases(self, feed_main_page, feed_page):
        with allure.step("Открытие ленты и получение начального значения «Выполнено за сегодня»"):
            feed_page.open_feed()
            counter_before = feed_page.get_counter_today()

        with allure.step("Оформление заказа на главной странице"):
            feed_main_page.open_main_page()
            feed_main_page.wait_page_loaded()
            feed_main_page.add_ingredient_to_order("Краторная булка N-200i")
            feed_main_page.add_ingredient_to_order("Соус Spicy-X")
            feed_main_page.submit_order()
            feed_main_page.close_order_modal()

        with allure.step("Проверка увеличения счётчика «Выполнено за сегодня»"):
            feed_page.open_feed()
            counter_after = feed_page.get_counter_today()

        assert counter_after > counter_before, (
            f"Счётчик «Выполнено за сегодня» не увеличился: "
            f"было {counter_before}, стало {counter_after}"
        )

    @allure.story("Заказ в разделе «В работе»")
    @allure.title("После оформления заказа он появляется в разделе «В работе»")
    @allure.description(
        "Проверяется, что оформленный заказ отображается в разделе «В работе». "
        "Тест создаёт заказ и убеждается, что он корректно появляется в ленте."
    )
    def test_order_in_work(self, feed_main_page, feed_page):
        with allure.step("Оформление заказа на главной странице"):
            feed_main_page.open_main_page()
            feed_main_page.wait_page_loaded()
            feed_main_page.add_ingredient_to_order("Краторная булка N-200i")
            feed_main_page.add_ingredient_to_order("Соус Spicy-X")
            feed_main_page.submit_order()

        allure.attach(
            "В модальном окне подтверждения заказа отображается значение "
            "счётчика «Выполнено за всё время», а не уникальный идентификатор заказа. "
            "Баг на стороне бэкенда: API возвращает счётчик вместо order ID.",
            name="Известный баг бэкенда: номер заказа = счётчик",
            attachment_type=allure.attachment_type.TEXT,
        )

        with allure.step("Закрытие модального окна и переход на ленту заказов"):
            feed_main_page.close_order_modal()
            feed_page.open_feed()

        with allure.step("Проверка, что заказ отображается в разделе «В работе»"):
            assert feed_page.is_order_in_work(), (
                "Заказ не появился в разделе «В работе»"
            )
