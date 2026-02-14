import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(type(self).__name__)

    def open_url(self, url):
        """Открытие страницы"""
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find_element(self, locator, time=10):
        """Поиск элемента с ожиданием"""
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Element not found: {locator}"
        )

    def click_element(self, locator, time=10):
        self.logger.info(f"Clicking element: {locator}")
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}"
        )
        element.click()

    def enter_text(self, locator, text, time=10):
        self.logger.info(f"Entering text '{text}' into: {locator}")
        element = self.find_element(locator, time)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator, time=10):
        element = self.find_element(locator, time)
        text = element.text
        self.logger.info(f"Text found: '{text}' in {locator}")
        return text