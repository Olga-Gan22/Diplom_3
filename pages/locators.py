from selenium.webdriver.common.by import By


class MainPageLocators:
    HEADER_CONSTRUCTOR_LINK = (
        By.CSS_SELECTOR, 
        "a.AppHeader_header__link__3D_hX"
    )

    FEED_BUTTON = (
        By.CSS_SELECTOR,
        "a[href='/feed']"
    )

    INGREDIENT_ITEM = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")
    INGREDIENT_NAME = (By.CSS_SELECTOR, "p.BurgerIngredient_ingredient__text__yp3dH")

    INGREDIENTS_LIST = (
        By.CSS_SELECTOR,
        "div.BurgerIngredients_ingredients__1NX8f"
    )

    MODAL_OPENED = (
        By.CSS_SELECTOR,
        "section.Modal_modal_opened__3ISw4"
    )
    MODAL_TITLE = (
        By.CSS_SELECTOR,
        "section.Modal_modal_opened__3ISw4 h2"
    )
    MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "button.Modal_modal__close__TnseK"
    )

    INGREDIENT_BY_NAME = (
        By.XPATH,
        "//a[contains(@class, 'BurgerIngredient_ingredient')][.//p[contains(text(), '{name}')]]"
    )

    INGREDIENT_COUNTER = (
        By.XPATH,
        "//a[contains(@class, 'BurgerIngredient_ingredient')][.//p[contains(text(), '{name}')]]//p[contains(@class, 'counter_counter__num')]"
    )

    CONSTRUCTOR_BASKET = (
        By.CSS_SELECTOR,
        "section.BurgerConstructor_basket__29Cd7"
    )
    CONSTRUCTOR_BASKET_LIST = (
        By.CSS_SELECTOR,
        "ul.BurgerConstructor_basket__list__l9dp_"
    )



class FeedPageLocators:
    # Ждём список «В работе» — он точно есть на странице
    FEED_TITLE = (
        By.CSS_SELECTOR,
        "ul.OrderFeed_orderListReady__1YFem"
    )

    # Ищем <p> с номером, который идёт сразу после <p> с текстом «Выполнено за все время:»
    COUNTER_TOTAL = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за все время:')]/following-sibling::p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )

    # Аналогично для «Выполнено за сегодня:»
    COUNTER_TODAY = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за сегодня:')]/following-sibling::p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )

    WORK_LIST_ITEM = (
        By.CSS_SELECTOR,
        "ul.OrderFeed_orderListReady__1YFem li"
    )


class AuthPageLocators:
    # Главная
    BTN_LOGIN_MAIN = (
        By.XPATH,
        "//button[contains(text(), 'Войти в аккаунт')]"
    )

    # Страница входа
    INPUT_EMAIL = (
        By.XPATH,
        "//label[text()='Email']/following-sibling::input"
    )
    INPUT_PASSWORD = (
        By.XPATH,
        "//label[text()='Пароль']/following-sibling::input"
    )
    BTN_SUBMIT_LOGIN = (
        By.CSS_SELECTOR,
        "button.button_button_type_primary__1O7Bx"
    )
    LINK_REGISTER_FROM_LOGIN = (
        By.CSS_SELECTOR,
        "a.Auth_link__1fOlj[href='/register']"
    )
    LOGIN_PAGE_HEADER = (
        By.XPATH,
        "//h2[text()='Вход']"
    )

    # Страница регистрации
    INPUT_REG_NAME = (
        By.XPATH,
        "//label[text()='Имя']/following-sibling::input"
    )
    INPUT_REG_EMAIL = (
        By.XPATH,
        "//label[text()='Email']/following-sibling::input"
    )
    INPUT_REG_PASSWORD = (
        By.CSS_SELECTOR,
        "input[type='password']"
    )
    BTN_REGISTER_SUBMIT = (
        By.CSS_SELECTOR,
        "button.button_button_type_primary__1O7Bx"
    )
    LINK_LOGIN_FROM_REGISTER = (
        By.CSS_SELECTOR,
        "a.Auth_link__1fOlj[href='/login']"
    )

    # Модальное окно (оверлей)
    MODAL_OVERLAY = (
        By.CSS_SELECTOR,
        "div.Modal_modal_overlay__x2ZCr"
    )

class OrderLocators:
    # Кнопка «Оформить заказ» — ищем по тексту и части класса типа кнопки
    BTN_ORDER = (
        By.XPATH,
        "//button[contains(@class, 'button_button_type_primary') and contains(text(), 'Оформить заказ')]"
    )

    # Модальное окно подтверждения заказа
    ORDER_MODAL = (
        By.CSS_SELECTOR,
        "div.Modal_modal__contentBox__sCy8X"
    )

    # Номер заказа — <h2> внутри модалки
    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "h2.Modal_modal__title__2L34m"
    )

    # Кнопка закрытия модалки (крестик)
    ORDER_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "button.Modal_modal__close__TnseK"
    )
