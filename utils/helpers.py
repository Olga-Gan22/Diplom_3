import allure
from pages.main_page import MainPage
from pages.auth_page import AuthPage


@allure.step("Оформить заказ с двумя ингредиентами и закрыть модальное окно")
def create_order_for_feed_tests(driver):
    """
    Выполняет ровно тот же сценарий, что сейчас прописан в тестах ленты:
      - открывает главную,
      - добавляет «Краторная булка N-200i» и «Соус Spicy-X»,
      - оформляет заказ,
      - закрывает модалку.
    Возвращает номер заказа.
    """
    page = MainPage(driver)
    page.open_main_page()
    page.wait_page_loaded()

    page.add_ingredient_to_order("Краторная булка N-200i")
    page.add_ingredient_to_order("Соус Spicy-X")

    order_number = page.submit_order()
    page.close_order_modal()

    return order_number


@allure.step("Зарегистрировать и авторизоваться новым пользователем")
def register_and_login(driver, user_data: dict):
    """
    Регистрирует пользователя и сразу выполняет вход.
    user_data — словарь с ключами name, email, password.
    """
    auth_page = AuthPage(driver)
    auth_page.register(
        name=user_data["name"],
        email=user_data["email"],
        password=user_data["password"],
    )
    auth_page.login(
        email=user_data["email"],
        password=user_data["password"],
    )
    return user_data
