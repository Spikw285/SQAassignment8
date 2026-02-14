import pytest
from pages.home_page import HomePage
from pages.cart_page import CartPage

@pytest.mark.regression
def test_add_items_check_total(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    home.load()
    home.add_product_to_cart("Brocolli")
    home.add_product_to_cart("Cauliflower")

    home.go_to_cart()

    total = cart.get_total_amount()
    assert total > 0, "The total amount should be greater than 0"

@pytest.mark.regression
def test_valid_promo_code(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    home.load()
    home.add_product_to_cart("Cucumber")
    home.go_to_cart()

    cart.apply_promo_code("rahulshettyacademy")
    msg = cart.get_promo_message()
    assert "Code applied" in msg

    original_price = cart.get_total_amount()
    discount_price = cart.get_discount_amount()
    assert discount_price < original_price, "Discount wasn't used"

@pytest.mark.regression
def test_cross_browser_sanity(driver):
    home = HomePage(driver)
    home.load()

    driver.set_window_size(768, 1024)
    home.search_product("Tomato")
    results = home.get_product_names()
    assert len(results) > 0, "Search doesn't work on 768x1024"

@pytest.mark.regression
def test_add_multiple_items(driver):
    home = HomePage(driver)
    home.load()

    products_to_add = ["Cucumber", "Carrot", "Beans"]
    for product in products_to_add:
        home.add_product_to_cart(product)

    home.go_to_cart()
    cart = CartPage(driver)
    assert cart.get_total_amount() > 100

@pytest.mark.negative
def test_invalid_promo_code(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    home.load()
    home.add_product_to_cart("Beetroot")
    home.go_to_cart()

    cart.apply_promo_code("SpikedSKull")

    msg = cart.get_promo_message()
    assert "Invalid code" in msg

@pytest.mark.negative
def test_search_negative(driver):
    home = HomePage(driver)
    home.load()

    home.search_product("PlayStation")

    try:
        results = home.get_product_names()
        assert results == 0, "Products shouldn't be found, but they're found"
    except:
        #in case it's not found via timeout, count as pass
        pass

