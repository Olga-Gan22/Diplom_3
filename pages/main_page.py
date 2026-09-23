import allure

from pages.base_page import BasePage
from pages.locators import MainPageLocators, OrderLocators, AuthPageLocators
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


@allure.feature("Главная страница")
@allure.description("Главная страница конструктора бургера: ингредиенты, модальные окна, оформление заказа")
class MainPage(BasePage):

    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        self.open(BASE_URL)

    @allure.step("Нажатие кнопки «Войти в аккаунт»")
    def click_login_button(self):
        self.wait_clickable(AuthPageLocators.BTN_LOGIN_MAIN).click()
        return self

    @allure.step("Переход в конструктор из шапки")
    def click_constructor_header_link(self):
        self.close_modal_overlay()
        self.wait_clickable(MainPageLocators.HEADER_CONSTRUCTOR_LINK).click()

    @allure.step("Переход в ленту заказов")
    def click_feed_button(self):
        self.close_modal_overlay()
        self.click(MainPageLocators.FEED_BUTTON)

    @allure.step("Клик по ингредиенту: {name}")
    def click_ingredient_by_name(self, name):
        self.close_modal_overlay()
        locator = (
            MainPageLocators.INGREDIENT_BY_NAME[0],
            MainPageLocators.INGREDIENT_BY_NAME[1].format(name=name),
        )
        self.click(locator)

    @allure.step("Проверка, что модальное окно открыто")
    def is_modal_opened(self):
        self.find(MainPageLocators.MODAL_OPENED)
        return True

    @allure.step("Проверка, что модальное окно закрыто")
    def is_modal_closed(self):
        self.wait_invisible(MainPageLocators.MODAL_OPENED)
        return True

    @allure.step("Получение заголовка модального окна")
    def get_modal_title_text(self):
        return self.get_text(MainPageLocators.MODAL_TITLE)

    @allure.step("Закрытие модального окна кнопкой «крестик»")
    def close_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.step("Получение количества ингредиента: {name}")
    def get_ingredient_counter(self, name):
        locator = (
            MainPageLocators.INGREDIENT_COUNTER[0],
            MainPageLocators.INGREDIENT_COUNTER[1].format(name=name),
        )
        return int(self.get_text(locator))

    @allure.step("Добавление ингредиента в заказ: {name} (через drag-and-drop)")
    def add_ingredient_to_order(self, name):
        ingredient_locator = (
            MainPageLocators.INGREDIENT_BY_NAME[0],
            MainPageLocators.INGREDIENT_BY_NAME[1].format(name=name),
        )
        source = self.find(ingredient_locator)
        target = self.find(MainPageLocators.CONSTRUCTOR_BASKET_LIST)
        self.scroll_to(MainPageLocators.CONSTRUCTOR_BASKET_LIST)
        self.execute_script(DRAG_DROP_SCRIPT, source, target)

    @allure.step("Ожидание полной загрузки страницы")
    def wait_page_loaded(self):
        self.find(MainPageLocators.INGREDIENT_ITEM)

    @allure.step("Оформление заказа (нажатие «Оформить заказ» и ожидание номера)")
    def submit_order(self):
        self.click_via_js(OrderLocators.BTN_ORDER)
        self.find(OrderLocators.ORDER_MODAL)
        self.wait_until(
            lambda d: d.find_element(*OrderLocators.ORDER_NUMBER).text.strip() not in ("", "9999"),
            condition_name="появился номер заказа в модальном окне"
        )
        order_number = self.get_text(OrderLocators.ORDER_NUMBER)
        return order_number

    @allure.step("Получение номера заказа из модального окна подтверждения")
    def get_order_number_from_modal(self):
        return self.get_text(OrderLocators.ORDER_NUMBER)

    @allure.step("Закрытие модального окна подтверждения заказа")
    def close_order_modal(self):
        self.click_via_js(OrderLocators.ORDER_CLOSE_BUTTON)
        self.wait_invisible(OrderLocators.ORDER_MODAL)
