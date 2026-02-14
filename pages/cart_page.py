from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    promo_input = (By.CSS_SELECTOR, "input.promoCode")
    promo_btn = (By.CSS_SELECTOR, "button.promoBtn")
    promo_info = (By.CSS_SELECTOR, "span.promoInfo")

    total_amount = (By.CSS_SELECTOR, ".totAmt")
    discount_amount = (By.CSS_SELECTOR, ".discountAmt")

    place_order_btn = (By.XPATH, "//button[text()='Place Order']")

    country_select = (By.TAG_NAME, "select")
    country_wrapper = (By.CSS_SELECTOR, ".wrapperTwo")
    chk_agree = (By.CSS_SELECTOR, "input.chkAgree")
    proceed_btn = (By.XPATH, "//button[text()='Proceed']")

    def apply_promo_code(self, code):
        self.enter_text(self.promo_input, code)
        self.click_element(self.promo_btn)

    def get_promo_message(self):
        return self.get_element_text(self.promo_info, time=15)

    def get_total_amount(self):
        return int(self.get_element_text(self.total_amount, time=15))

    def get_discount_amount(self):
        return float(self.get_element_text(self.discount_amount, time=15))