import pytest
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
@pytest.mark.smoke
def test_open_greenkart(driver):
    home_page = HomePage(driver)
    home_page.load()

    assert "GreenKart" in driver.title, ("Page title doesn't contain "
                                         "Greenkart'")

@pytest.mark.smoke
def test_search_func(driver):
    home_page = HomePage(driver)
    home_page.load()

    home_page.search_product("Cucumber")

    results = home_page.get_product_names()

    print(f"Found {results} products")

    assert len(results) > 0, "No products found"
    assert "Cucumber" in results[0], f"Waited for Cucumber, got {results[0]}"

@pytest.mark.smoke
def test_cart_is_empty_initially(driver):
    home_page = HomePage(driver)
    home_page.load()

    items_count = home_page.get_element_text((By.CSS_SELECTOR, ".cart-info tr:nth-child(1) strong"))
    assert int(items_count) == 0, "Cart is not empty initially"

@pytest.mark.smoke
def test_top_deals_link(driver):
    home_page = HomePage(driver)
    home_page.load()

    home_page.click_element((By.LINK_TEXT, "Top Deals"))

    driver.switch_to.window(driver.window_handles[1])
    assert "GreenKart" in driver.title

    driver.close()
    driver.switch_to.window(driver.window_handles[0])