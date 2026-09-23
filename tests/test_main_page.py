import allure
from config.urls import MAIN_PAGE_URL, CONSTRUCTOR_URL, FEED_URL, LOGIN_URL, BASE_URL


@allure.feature("Навигация и базовая функциональность")
@allure.description("Тесты главной страницы: навигация, модальные окна, счётчики ингредиентов")
class TestMainPage:

    @allure.story("Кнопка «Конструктор»: сценарий через ленту заказов")
    @allure.title("Главная → «Лента заказов» → «Конструктор» → Главная")
    @allure.description(
        "Сценарий: с главной страницы переходим в ленту заказов, "
        "затем нажимаем «Конструктор» в шапке и проверяем, что вернулись на главную."
    )
    def test_constructor_link_via_feed_flow(self, main_page):
        with allure.step("1. Открываем главную страницу"):
            main_page.open_main_page()
            main_page.wait_page_loaded()

        with allure.step("2. Нажимаем «Лента заказов» в шапке"):
            main_page.click_feed_button()

        with allure.step("3. Проверяем, что попали на страницу ленты заказов"):
            current_url = main_page.get_current_url()
            assert "/feed" in current_url, f"Ожидался URL ленты заказов, но получен: {current_url}"

        with allure.step("4. Нажимаем кнопку «Конструктор» в шапке"):
            main_page.click_constructor_header_link()

        with allure.step("5. Проверяем, что вернулись на главную"):
            current_url = main_page.get_current_url()
            normalized_url = current_url.rstrip("/")
            expected_url = BASE_URL.rstrip("/")

            assert normalized_url == expected_url, (
                f"Ожидался переход на главную (конструктор), но получен URL: {current_url}"
            )

    @allure.story("Переход по кнопке «Лента Заказов»")
    @allure.title("Переход по клику на раздел «Лента заказов»")
    @allure.description(
        "Проверяется переход на страницу «Лента заказов» по клику на соответствующую кнопку. "
        "Убеждаемся, что URL страницы совпадает с ожидаемым адресом ленты."
    )
    def test_click_feed_button(self, main_page):
        with allure.step("Клик по кнопке «Лента Заказов»"):
            main_page.click_feed_button()

        with allure.step("Проверка URL страницы ленты заказов"):
            current_url = main_page.get_current_url()
            assert current_url == FEED_URL or "/feed" in current_url, \
                f"Ожидался URL ленты, но получен: {current_url}"

    @allure.story("Всплывающее окно ингредиента")
    @allure.title("При клике на ингредиент открывается модальное окно с деталями")
    @allure.description(
        "При клике на конкретный ингредиент должно открываться модальное окно. "
        "Тест проверяет факт появления окна и корректность его заголовка («Детали ингредиента»)."
    )
    def test_ingredient_modal_opened(self, main_page):
        ingredient_name = "Соус Spicy-X"

        with allure.step(f"Клик по ингредиенту: {ingredient_name}"):
            main_page.click_ingredient_by_name(ingredient_name)

        with allure.step("Ожидание открытия модального окна"):
            assert main_page.is_modal_opened(), "Модальное окно не открылось"

        with allure.step("Проверка заголовка модального окна"):
            title = main_page.get_modal_title_text()
            assert "детали" in title.lower(), f"Неверный заголовок модального окна: {title}"

    @allure.story("Закрытие всплывающего окна")
    @allure.title("Модальное окно закрывается кликом по крестику")
    @allure.description(
        "Проверяется корректное закрытие модального окна при нажатии на кнопку-крестик. "
        "Тест убеждается, что окно действительно исчезает со страницы."
    )
    def test_ingredient_modal_closed(self, main_page):
        ingredient_name = "Соус Spicy-X"

        with allure.step(f"Клик по ингредиенту: {ingredient_name} для открытия окна"):
            main_page.click_ingredient_by_name(ingredient_name)

        with allure.step("Закрытие модального окна кнопкой «крестик»"):
            main_page.close_modal()

        with allure.step("Подтверждение, что окно закрыто"):
            assert main_page.is_modal_closed(), "Модальное окно осталось открытым"

    @allure.story("Счётчик ингредиента")
    @allure.title("При добавлении начинки счётчик увеличивается")
    @allure.description(
        "Тест проверяет логику счётчика ингредиентов: после добавления ингредиента в заказ "
        "значение счётчика должно увеличиться. Сравниваются значения до и после действия."
    )
    def test_ingredient_counter_increases(self, main_page):
        name = "Соус Spicy-X"

        with allure.step(f"Получение начального значения счётчика для: {name}"):
            counter_before = main_page.get_ingredient_counter(name)
            assert counter_before is not None, f"Не удалось получить счётчик для {name}"

        with allure.step(f"Добавление ингредиента: {name} в заказ (drag-and-drop)"):
            main_page.add_ingredient_to_order(name)

        with allure.step(f"Получение обновлённого значения счётчика"):
            counter_after = main_page.get_ingredient_counter(name)
            assert counter_after is not None, f"Не удалось получить обновлённый счётчик для {name}"

        with allure.step("Сравнение значений: счётчик должен увеличиться"):
            assert counter_after > counter_before, (
                f"Счётчик не увеличился: было {counter_before}, стало {counter_after}"
            )
