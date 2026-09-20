from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def wait_for_order_in_work(driver, timeout=15):
    """
    Ждём, пока из списка исчезнет текст «Все текущие заказы готовы!».
    Это самый надёжный способ: мы ждём конкретного изменения, а не «чего-то там».
    """
    locator = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem")
    text_to_disappear = "готовы"

    def text_disappeared(driver):
        el = driver.find_element(*locator)
        return text_to_disappear not in el.text.lower()

    return WebDriverWait(driver, timeout).until(text_disappeared)
