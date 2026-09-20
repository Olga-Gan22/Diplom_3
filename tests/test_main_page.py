import allure
from config.urls import MAIN_PAGE_URL, FEED_PAGE_URL


@allure.feature("Навигация и базовая функциональность")
class TestMainPage:

    @allure.story("Переход по кнопке «Конструктор»")
    @allure.title("Переход по клику на «Конструктор»")
    @allure.description(
        "Проверяется, что при клике на кнопку «Конструктор» происходит переход на страницу конструктора. "
        "Тест подтверждает корректную работу навигационной кнопки и соответствие URL целевому адресу."
    )
    def test_click_constructor_button(self, main_page):
        with allure.step("Клик по кнопке «Конструктор»"):
            main_page.click_constructor_button()
        
        with allure.step("Проверка, что URL соответствует главной странице"):
            assert main_page.get_current_url() == MAIN_PAGE_URL

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
            assert main_page.get_current_url() == FEED_PAGE_URL

    @allure.story("Всплывающее окно ингредиента")
    @allure.title("При клике на ингредиент открывается модальное окно с деталями")
    @allure.description(
        "При клике на конкретный ингредиент должно открываться модальное окно. "
        "Тест проверяет факт появления окна и корректность его заголовка («Детали ингредиента»)."
    )
    def test_ingredient_modal_opened(self, main_page):
        ingredient_name = "Флюоресцентная булка R2-D3"
        
        with allure.step(f"Клик по ингредиенту: {ingredient_name}"):
            main_page.click_ingredient_by_name(ingredient_name)
        
        with allure.step("Ожидание открытия модального окна"):
            assert main_page.is_modal_opened()
        
        with allure.step("Проверка заголовка модального окна"):
            assert main_page.get_modal_title_text() == "Детали ингредиента"

    @allure.story("Закрытие всплывающего окна")
    @allure.title("Модальное окно закрывается кликом по крестику")
    @allure.description(
        "Проверяется корректное закрытие модального окна при нажатии на кнопку-крестик. "
        "Тест убеждается, что окно действительно исчезает со страницы."
    )
    def test_ingredient_modal_closed(self, main_page):
        ingredient_name = "Флюоресцентная булка R2-D3"
        
        with allure.step(f"Клик по ингредиенту: {ingredient_name} для открытия окна"):
            main_page.click_ingredient_by_name(ingredient_name)
        
        with allure.step("Закрытие модального окна кнопкой «крестик»"):
            main_page.close_modal()
        
        with allure.step("Подтверждение, что окно закрыто"):
            assert main_page.is_modal_closed()

    @allure.story("Счётчик ингредиента")
    @allure.title("При добавлении начинки счётчик увеличивается")
    @allure.description(
        "Тест проверяет логику счётчика ингредиентов: после добавления ингредиента в заказ "
        "значение счётчика должно увеличиться. Сравниваются значения до и после действия."
    )
    def test_ingredient_counter_increases(self, main_page):
        name = "Говяжий метеорит (отбивная)"  
        
        with allure.step(f"Получение начального значения счётчика для: {name}"):
            counter_before = main_page.get_ingredient_counter(name)
        
        with allure.step(f"Добавление ингредиента: {name} в заказ (drag-and-drop)"):
            main_page.add_ingredient_to_order(name)
        
        with allure.step(f"Получение обновлённого значения счётчика"):
            counter_after = main_page.get_ingredient_counter(name)
        
        with allure.step("Сравнение значений: счётчик должен увеличиться"):
            assert counter_after > counter_before
