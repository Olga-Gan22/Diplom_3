import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from pages.locators import MainPageLocators, OrderLocators
from config.urls import BASE_URL


DRAG_DROP_SCRIPT = """
function simulateDragDrop(sourceNode, targetNode) {
    const EVENT_TYPES = {
        DRAG_START: 'dragstart',
        DRAG_END: 'dragend',
        DRAG_ENTER: 'dragenter',
        DRAG_OVER: 'dragover',
        DRAG_LEAVE: 'dragleave',
        DROP: 'drop'
    };

    function createCustomEvent(type) {
        const event = document.createEvent('CustomEvent');
        event.initCustomEvent(type, true, true, null);
        event.dataTransfer = {
            data: {},
            setData: function(type, val) { this.data[type] = val; },
            getData: function(type) { return this.data[type]; }
        };
        return event;
    }

    const dragStartEvent = createCustomEvent(EVENT_TYPES.DRAG_START);
    const dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
    const dropEvent = createCustomEvent(EVENT_TYPES.DROP);
    const dragEnterEvent = createCustomEvent(EVENT_TYPES.DRAG_ENTER);
    const dragOverEvent = createCustomEvent(EVENT_TYPES.DRAG_OVER);
    const dragLeaveEvent = createCustomEvent(EVENT_TYPES.DRAG_LEAVE);

    sourceNode.dispatchEvent(dragStartEvent);
    targetNode.dispatchEvent(dragEnterEvent);
    targetNode.dispatchEvent(dragOverEvent);
    targetNode.dispatchEvent(dropEvent);
    sourceNode.dispatchEvent(dragEndEvent);
}
simulateDragDrop(arguments[0], arguments[1]);
"""


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ------------------------------------------------------------
    # Навигация и базовые методы
    # ------------------------------------------------------------

    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        self.driver.get(BASE_URL)

    @allure.step("Получение текущего URL страницы")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Переход в Конструктор")
    def click_constructor_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.CONSTRUCTOR_BUTTON)
        )
        button.click()

    @allure.step("Переход в Ленту заказов")
    def click_feed_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.FEED_BUTTON)
        )
        button.click()

    # ------------------------------------------------------------
    # Модальное окно ингредиента
    # ------------------------------------------------------------

    @allure.step("Клик по ингредиенту: {name}")
    def click_ingredient_by_name(self, name):
        locator = (
            MainPageLocators.INGREDIENT_BY_NAME[0],
            MainPageLocators.INGREDIENT_BY_NAME[1].format(name=name),
        )
        ingredient = self.wait.until(EC.element_to_be_clickable(locator))
        ingredient.click()

    @allure.step("Проверка, что модальное окно открыто")
    def is_modal_opened(self):
        self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_OPENED)
        )
        return True

    @allure.step("Проверка, что модальное окно закрыто")
    def is_modal_closed(self):
        self.wait.until(
            EC.invisibility_of_element_located(MainPageLocators.MODAL_OPENED)
        )
        return True

    @allure.step("Получение заголовка модального окна")
    def get_modal_title_text(self):
        title = self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_TITLE)
        )
        return title.text

    @allure.step("Закрытие модального окна кнопкой «крестик»")
    def close_modal(self):
        close_btn = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
        )
        close_btn.click()

    # ------------------------------------------------------------
    # Счётчик ингредиента
    # ------------------------------------------------------------

    @allure.step("Получение количества ингредиента: {name}")
    def get_ingredient_counter(self, name):
        locator = (
            MainPageLocators.INGREDIENT_COUNTER[0],
            MainPageLocators.INGREDIENT_COUNTER[1].format(name=name),
        )
        counter = self.wait.until(EC.visibility_of_element_located(locator))
        return int(counter.text)

    # ------------------------------------------------------------
    # Drag-and-drop
    # ------------------------------------------------------------

    @allure.step("Добавление ингредиента в заказ: {name} (через drag-and-drop)")
    def add_ingredient_to_order(self, name):
        ingredient_locator = (
            MainPageLocators.INGREDIENT_BY_NAME[0],
            MainPageLocators.INGREDIENT_BY_NAME[1].format(name=name),
        )

        source = self.wait.until(EC.visibility_of_element_located(ingredient_locator))
        target = self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_BASKET_LIST)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'auto'});", target
        )
        time.sleep(0.5)

        self.driver.execute_script(DRAG_DROP_SCRIPT, source, target)

    # ------------------------------------------------------------
    # Ожидание загрузки
    # ------------------------------------------------------------

    @allure.step("Ожидание полной загрузки страницы")
    def wait_page_loaded(self):
        self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.INGREDIENTS_LIST)
        )

    # ------------------------------------------------------------
    # Оформление заказа
    # ------------------------------------------------------------

    @allure.step("Оформление заказа (нажатие «Оформить заказ» и ожидание номера)")
    def submit_order(self):
        # Даём React время «увидеть» ингредиент в корзине
        time.sleep(2)

        btn = self.wait.until(
            EC.element_to_be_clickable(OrderLocators.BTN_ORDER)
        )
        btn.click()

        # Ждём появления модалки
        self.wait.until(
            EC.visibility_of_element_located(OrderLocators.ORDER_MODAL)
        )

        # Ждём, пока номер сменится с заглушки '9999' на реальный
        def number_is_real(driver):
            el = driver.find_element(*OrderLocators.ORDER_NUMBER)
            text = el.text.strip()
            return text and text != "9999"

        real_number = WebDriverWait(self.driver, 20).until(number_is_real)
        return real_number

    @allure.step("Закрытие модального окна подтверждения заказа")
    def close_order_modal(self):
        """Закрывает модалку с подтверждением заказа через JS-клик."""
        btn = self.wait.until(
            EC.element_to_be_clickable(OrderLocators.ORDER_CLOSE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(
            EC.invisibility_of_element_located(OrderLocators.ORDER_MODAL)
        )
