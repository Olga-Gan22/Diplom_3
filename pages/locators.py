from selenium.webdriver.common.by import By


class MainPageLocators:
    # Кнопка «Конструктор» в хедере
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and .//p[text()='Конструктор']]")

    # Кнопка «Лента Заказов» в хедере
    FEED_BUTTON = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and .//p[text()='Лента Заказов']]")

    # Список ингредиентов
    INGREDIENTS_LIST = (By.CLASS_NAME, "BurgerIngredients_ingredients__list__2A-mT")

    # Карточка ингредиента по имени
    INGREDIENT_BY_NAME = (
        By.XPATH,
        "//a[contains(@class, 'BurgerIngredient_ingredient') and p[text()='{name}']]"
    )

    # Счётчик внутри карточки ингредиента
    INGREDIENT_COUNTER = (
        By.XPATH,
        "//a[contains(@class, 'BurgerIngredient_ingredient') and p[text()='{name}']]//p[contains(@class, 'counter_counter__num')]"
    )

    # Модальное окно (открытое)
    MODAL_OPENED = (By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4")

    # Модальное окно (закрытое / отсутствует)
    MODAL_CLOSED = (By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4[style*='pointer-events: none']")

    # Заголовок модального окна
    MODAL_TITLE = (By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4 h2")

    # Кнопка закрытия модального окна (крестик)
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")

    # Корзина конструктора (зона для drag-and-drop)
    CONSTRUCTOR_BASKET = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")

    # Тело корзины (для drop-target)
    CONSTRUCTOR_BASKET_LIST = (By.CSS_SELECTOR, "ul.BurgerConstructor_basket__list__l9dp_")



class FeedPageLocators:
    # Заголовок страницы «Лента заказов»
    FEED_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")

    # Счётчик «Выполнено за все время»
    COUNTER_TOTAL = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за все время')]/following::p[contains(@class, 'OrderFeed_number__2MbrQ')][1]"
    )

    # Счётчик «Выполнено за сегодня»
    COUNTER_TODAY = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за сегодня')]/following::p[contains(@class, 'OrderFeed_number__2MbrQ')][1]"
    )

    # Список «В работе» (когда пусто — внутри текст «Все текущие заказы готовы!»)
    WORK_LIST = (
        By.CSS_SELECTOR,
        "ul.OrderFeed_orderListReady__1YFem"
    )


class AuthPageLocators:
    # Главная
    BTN_LOGIN_MAIN = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")

    # Страница входа
    INPUT_EMAIL = (By.CSS_SELECTOR, "input[name='name']")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    BTN_SUBMIT_LOGIN = (By.XPATH, "//button[contains(text(), 'Войти')]")
    LINK_REGISTER_FROM_LOGIN = (
        By.XPATH, "//a[contains(@href, '/register') and contains(text(), 'Зарегистрироваться')]"
    )
    LOGIN_PAGE_HEADER = (By.CSS_SELECTOR, "h1[data-testid='login-header']")

    # Страница регистрации
    INPUT_REG_NAME = (By.XPATH, "//label[contains(text(), 'Имя')]/following::input[1]")
    INPUT_REG_EMAIL = (By.XPATH, "//label[contains(text(), 'Email')]/following::input[1]")
    INPUT_REG_PASSWORD = (By.CSS_SELECTOR, "input[name='Пароль']")
    BTN_REGISTER_SUBMIT = (By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]")
    LINK_LOGIN_FROM_REGISTER = (
        By.XPATH, "//a[contains(@href, '/login') and contains(text(), 'Войти')]"
    )

    # Модальное окно (оверлей) — для закрытия всплывашек
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr")


class OrderLocators:
    # Кнопка «Оформить заказ»
    BTN_ORDER = (
        By.XPATH,
        "//button[contains(text(), 'Оформить заказ')] | //a[contains(text(), 'Оформить заказ')]"
    )

    # Модальное окно с подтверждением заказа
    ORDER_MODAL = (By.CSS_SELECTOR, "div.Modal_modal__contentBox__sCy8X")

    # Номер заказа — <h2> внутри модалки
    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "h2.Modal_modal__title__2L34m"
    )

    # Кнопка закрытия (крестик)
    ORDER_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "button.Modal_modal__close__TnseK"
    )

