import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
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