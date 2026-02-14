from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

class HomePage(BasePage):
    URL = "https://rahulshettyacademy.com/seleniumPractise/#/"

    PRODUCTS_LOCATOR = (By.CSS_SELECTOR, "div.products div.product")
    PRODUCT_NAME_LOCATOR = (By.CSS_SELECTOR, "h4.product-name")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search-button")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "h4.product-name")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//div[@class='product-action']/button")
    CART_ICON = (By.CSS_SELECTOR, "a.cart-icon")
    PROCEED_TO_CHECKOUT_BTN = (By.XPATH, "//button[text()='PROCEED TO CHECKOUT']")

    PRODUCT_ADD_BUTTON_XPATH = "//h4[contains(text(), '{}')]/parent::div//button"

    def load(self):
        self.open_url(self.URL)

    def search_product(self, product_name):
        elem = self.driver.find_element(*self.SEARCH_INPUT)
        elem.clear()
        elem.send_keys(product_name)
        try:
            btn = self.driver.find_element(*self.SEARCH_BUTTON)
            btn.click()
        except Exception:
            pass

    def get_product_names(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            products = wait.until(EC.presence_of_all_elements_located(self.PRODUCTS_LOCATOR))
            names = []
            for p in products:
                try:
                    name = p.find_element(*self.PRODUCT_NAME_LOCATOR).text
                    names.append(name.strip())
                except StaleElementReferenceException:
                    products = wait.until(EC.presence_of_all_elements_located(self.PRODUCTS_LOCATOR))
                    names = [q.find_element(*self.PRODUCT_NAME_LOCATOR).text.strip() for q in products]
                    break
            return names
        except TimeoutException:
            return []
    def add_product_to_cart(self, product_name):
        xpath = self.PRODUCT_ADD_BUTTON_XPATH.format(product_name)
        self.click_element((By.XPATH, xpath))

    def go_to_cart(self):
        self.click_element(self.CART_ICON)
        self.click_element(self.PROCEED_TO_CHECKOUT_BTN)