import re
import pytest
from pages.home_page import HomePage
from pages.cart_page import CartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.smoke
def test_open_greenkart(driver):
    home_page = HomePage(driver)
    home_page.load()
    assert "GreenKart" in driver.title or "Greenkart" in driver.title, "Page title doesn't contain expected substring"

@pytest.mark.smoke
def test_search_func(driver):
    home_page = HomePage(driver)
    home_page.load()
    home_page.search_product("Cucumber")

    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: len(home_page.get_product_names()) > 0)

    results = home_page.get_product_names()
    assert len(results) > 0, "No products found"
    assert "cucumber" in results[0].lower(), f"Expected 'Cucumber' in first result, got: {results[0]}"

@pytest.mark.smoke
def test_cart_is_empty_initially(driver):
    home_page = HomePage(driver)
    home_page.load()
    text = home_page.get_element_text((By.CSS_SELECTOR, ".cart-info tr:nth-child(1) strong"))
    m = re.search(r"\d+", text or "")
    count = int(m.group()) if m else 0
    assert count == 0, f"Cart is not empty initially (found {count})"

@pytest.mark.smoke
def test_top_deals_link(driver):
    home_page = HomePage(driver)
    home_page.load()
    home_page.click_element((By.LINK_TEXT, "Top Deals"))
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) >= 2)
    handles = driver.window_handles
    assert len(handles) >= 2, "Top Deals did not open a new tab/window"
    driver.switch_to.window(handles[-1])
    assert "GreenKart" in driver.title or "Top" in driver.title, "Unexpected title in Top Deals window"
    driver.close()
    driver.switch_to.window(handles[0])

@pytest.mark.smoke
def test_add_to_cart_and_proceed_smoke(driver):
    """
    Smoke: add one product and proceed to checkout
    """
    home = HomePage(driver)
    cart = CartPage(driver)

    home.load()
    home.add_product_to_cart("Cucumber")
    home.go_to_cart()

    total = cart.get_total_amount()
    assert total > 0, f"Expected total > 0 after adding item, got {total}"
