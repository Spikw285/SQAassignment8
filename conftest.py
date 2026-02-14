import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FFService
from webdriver_manager.firefox import GeckoDriverManager

def _build_chrome(headless=False, width=1366, height=768):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def _build_firefox(headless=False, width=1366, height=768):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    service = FFService(GeckoDriverManager().install())
    drv = webdriver.Firefox(service=service, options=options)
    drv.set_window_size(width, height)
    return drv

@pytest.fixture(scope="function")
def driver(request):
    browser = os.environ.get("BROWSER", "chrome").lower()
    headless = os.environ.get("HEADLESS", "true").lower() in ("1","true","yes")
    viewport = os.environ.get("VIEWPORT", "desktop").lower()
    if viewport == "mobile":
        width, height = 768, 1024
    else:
        width, height = 1366, 768

    if browser == "firefox":
        drv = _build_firefox(headless=headless, width=width, height=height)
    else:
        drv = _build_chrome(headless=headless, width=width, height=height)

    yield drv
    try:
        drv.quit()
    except Exception:
        pass


from datetime import datetime
import os
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when in ('call', 'setup'):
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            driver = item.funcargs.get('driver', None)
            if driver:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                screenshot_name = f"screenshot_{timestamp}.png"
                reports_dir = os.path.join(os.getcwd(), 'reports', 'screenshots')
                os.makedirs(reports_dir, exist_ok=True)
                screenshot_path = os.path.join(reports_dir, screenshot_name)
                driver.save_screenshot(screenshot_path)
                if pytest_html:
                    extra.append(pytest_html.extras.image(f"screenshots/{screenshot_name}"))
        report.extra = extra
