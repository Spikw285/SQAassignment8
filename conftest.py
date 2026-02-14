import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FFService
from webdriver_manager.firefox import GeckoDriverManager


# ---------- CLI OPTIONS ----------

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome or firefox"
    )
    parser.addoption(
        "--viewport",
        action="store",
        default="desktop",
        help="Viewport: desktop or mobile"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Headless mode: true or false"
    )


# ---------- DRIVER FIXTURE ----------

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    viewport = request.config.getoption("--viewport").lower()
    headless = request.config.getoption("--headless").lower() in ("true", "1", "yes")

    # viewport sizes
    if viewport == "mobile":
        width, height = 768, 1024
    else:
        width, height = 1366, 768

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FFService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(width, height)

    else:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()
