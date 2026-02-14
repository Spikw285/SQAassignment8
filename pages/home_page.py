from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):
    URL = "https://rahulshettyacademy.com/seleniumPractise/#/"

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
        self.enter_text(self.SEARCH_INPUT, product_name)
        self.click_element(self.SEARCH_BUTTON)

    def get_product_names(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.PRODUCT_NAMES)
        )
        products = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [p.text for p in products]

    def add_product_to_cart(self, product_name):
        xpath = self.PRODUCT_ADD_BUTTON_XPATH.format(product_name)
        self.click_element((By.XPATH, xpath))

    def go_to_cart(self):
        self.click_element(self.CART_ICON)
        self.click_element(self.PROCEED_TO_CHECKOUT_BTN)